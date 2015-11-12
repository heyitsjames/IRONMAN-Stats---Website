import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from .models import Race, RaceResult


class Webdriver:

    def __init__(self):
        # get the Firefox profile object
        firefox_profile = FirefoxProfile()
        # Disable CSS
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        # Disable images
        firefox_profile.set_preference('permissions.default.image', 2)
        # Disable Flash
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        # Use the driver
        self.driver = webdriver.Firefox(firefox_profile)
        self.driver.implicitly_wait(3)  # seconds
        self.race = None
        self.race_distance = ''
        self.gender = ''
        self.age_group = ''
        self.filter_query_string = '#mainContentCol4 .moduleContentInner .filters .genderSelect'
        self.ironman_urls = ["http://www.ironman.com/events/triathlon-races.aspx?d=ironman",
                             "http://www.ironman.com/events/triathlon-races.aspx?d=ironman+70.3"]

    def run(self):
        # TODO: Crawl both distances
        for url in self.ironman_urls[1:]:
            self.crawl_ironman(url)
        self.driver.close()

    def crawl_ironman(self, url):
        self.driver.get(url)

        event_urls = self.driver.find_elements_by_css_selector('a.eventDetails')
        event_result_urls = [(event_url.get_attribute(name='href')
                              .replace('.aspx', '/results.aspx')) for event_url in event_urls]

        for result_url in event_result_urls:
            self.crawl_race(result_url)

    def crawl_race(self, results_url):
        self.driver.get(results_url)

        self.race_distance = (Race.DISTANCES['full-ironman'] if
                              re.split(r'/events/\w+/(.+)/', results_url)[1] == 'ironman' else
                              Race.DISTANCES['half-ironman'])

        race_years = self.driver.find_elements_by_css_selector('nav.rResultswWrap ul li a')
        race_links = [r.get_attribute(name='href') for r in race_years]

        try:
            filter_controls_available = self.driver.find_element_by_css_selector(
                self.filter_query_string).is_displayed()
        except NoSuchElementException:
            return

        if not race_years and filter_controls_available:
            race_links = [results_url]

        for race_link in race_links:
            self.crawl_race_year(race_link)

    def crawl_race_year(self, race_link):
        self.driver.get(race_link)
        # if the filtering controls aren't visible, then we can't
        # reliably parse the race, so we'll just fail silently here
        try:
            filter_controls_available = self.driver.find_element_by_css_selector(
                self.filter_query_string).is_displayed()
        except NoSuchElementException:
            return

        if filter_controls_available:
            age_group_list = [age[0] for age in RaceResult.AGE_GROUPS]
            gender_list = [gender[0] for gender in RaceResult.SEXES]

            date_and_name = self.driver.find_element_by_css_selector(
                '.moduleContentInner header h1').get_attribute(name='innerHTML')
            string_date = date_and_name.split(' ')[0]
            race_date, race_name = (datetime.strptime(string_date, '%m/%d/%Y').date(),
                                    date_and_name.split('&nbsp;')[1])

            self.race, created = Race.objects.get_or_create(title=race_name,
                                                            distance=self.race_distance,
                                                            date=race_date)
            if not created:
                return  # This race has already been crawled. Sally forth!

            for gender in gender_list:
                for age_group in age_group_list:
                    if race_link[-1] != '?':
                        race_link = race_link + '?'
                    url_params_string = '{0}&agegroup={1}&sex={2}&p=1&ps=4000'

                    composite_url = url_params_string.format(race_link, age_group, gender)

                    # so we don't have to pass them along
                    self.gender = gender
                    self.age_group = age_group

                    self.crawl_gender_and_age_group(composite_url)

    def crawl_gender_and_age_group(self, composite_url):
        self.driver.get(composite_url)

        try:
            name_link = self.driver.find_element_by_css_selector(
                '#eventResults thead th.name a')
        except NoSuchElementException:
            return  # no athletes in that age group

        name_link.click()
        time.sleep(5)
        athlete_rows = self.driver.find_elements_by_css_selector(
            '#eventResults tbody tr')

        athlete_list = [self.create_athlete_data(row) for row in athlete_rows]
        RaceResult.objects.bulk_create(athlete_list)

    def create_athlete_data(self, row):
        keys = ['athlete_name', 'athlete_country', 'division_rank',
                'gender_rank', 'overall_rank', 'swim_time', 'bike_time',
                'run_time', 'finish_time', 'points']
        try:
            values = [v.text for v in row.find_elements_by_css_selector('td')]
        except:
            self.create_athlete_data(row)

        athlete_dict = {k: v for k, v in zip(keys, values)}
        for key, value in athlete_dict.items():
            if value == '---':
                athlete_dict[key] = None
                continue
            if key in ['swim_time', 'bike_time', 'run_time', 'finish_time']:
                if key == 'finish_time':
                    if value == 'DNS' or value == 'DNF' or value == 'DQ':
                        # set the finish time to None, and set the race_status to DNS or DNF
                        athlete_dict[key] = None
                        race_status = value
                    else:
                        race_status = RaceResult.RACE_STATUSES['Finished']
                if athlete_dict[key] is not None:
                    try:
                        athlete_dict[key] = datetime.strptime(athlete_dict[key], '%H:%M:%S').time()
                    except ValueError:  # probably a weird format
                        athlete_dict[key] = None

        return RaceResult(race_id=self.race.id,
                          race_status=race_status,
                          age_group=self.age_group,
                          sex=self.gender,
                          **athlete_dict)
