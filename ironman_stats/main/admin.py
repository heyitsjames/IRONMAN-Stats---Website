from django.contrib import admin
from ironman_stats.main.models import ComputedRaceData, Race, RaceResult


class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('race', 'athlete_name', 'age_group', 'sex',
                    'athlete_country', 'str_finish_time', 'race_status')

    search_fields = ['race__title', 'athlete_name']


class RaceAdmin(admin.ModelAdmin):
    search_fields = ['title']


class ComputedRaceDataAdmin(admin.ModelAdmin):
    list_display = ('race', 'age_group', 'sex')


admin.site.register(RaceResult, RaceResultAdmin)
admin.site.register(Race, RaceAdmin)
admin.site.register(ComputedRaceData, ComputedRaceDataAdmin)
