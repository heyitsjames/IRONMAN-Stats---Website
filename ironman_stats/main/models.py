from django.db import models
from model_utils import Choices


class Race(models.Model):
    DISTANCES = Choices('half-ironman', 'full-ironman',)
    distance = models.CharField(choices=DISTANCES, max_length=40)
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
            return '{0} {1}'.format(self.title, self.date.year)

    class Meta:
        unique_together = ('distance', 'title', 'date',)


class RaceResult(models.Model):
    AGE_GROUPS = Choices('Pro', '18-24', '25-29', '30-34', '35-39',
                         '40-44', '45-49', '50-54', '55-59', '60-64',
                         '65-69', '70-74', '75-79', '80-999')
    SEXES = Choices('M', 'F')
    RACE_STATUSES = Choices('DQ', 'DNS', 'DNF', 'Finished')
    race = models.ForeignKey(Race)
    athlete_name = models.CharField(max_length=255)
    age_group = models.CharField(max_length=255, choices=AGE_GROUPS)
    sex = models.CharField(max_length=1, choices=SEXES)
    athlete_country = models.CharField(max_length=255, blank=True, null=True)
    division_rank = models.IntegerField(blank=True, null=True,)
    gender_rank = models.IntegerField(blank=True, null=True,)
    overall_rank = models.IntegerField(blank=True, null=True,)
    swim_time = models.TimeField(blank=True, null=True,)
    bike_time = models.TimeField(blank=True, null=True,)
    run_time = models.TimeField(blank=True, null=True,)
    finish_time = models.TimeField(blank=True, null=True,)
    points = models.IntegerField(blank=True, null=True,)
    race_status = models.CharField(choices=RACE_STATUSES,
                                   default=RACE_STATUSES['Finished'], max_length=40)

    def my_property(self):
            return self.first_name + ' ' + self.last_name

    def finish_time_as_string(self):
        return self.finish_time.strftime('%H:%M:%S') if self.finish_time else '---'
    finish_time_as_string.short_description = "finish time"

    str_finish_time = property(finish_time_as_string)

    def __str__(self):
            return '{0} - {1}'.format(self.athlete_name, self.finish_time)
