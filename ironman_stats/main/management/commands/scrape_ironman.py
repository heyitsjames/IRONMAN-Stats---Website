from django.core.management.base import BaseCommand
from ironman_stats.main.webdriver import Webdriver


class Command(BaseCommand):
    help = 'Scrapes ironman.com for all the data. All of it.'

    def handle(self, *args, **options):
        webdriver = Webdriver()
        webdriver.run()
