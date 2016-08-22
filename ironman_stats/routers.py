from rest_framework import routers

from ironman_stats.main.api import (ComputedRaceDataViewSet, RaceResultViewSet,
                                    RaceTitleViewSet, RaceViewSet)

router = routers.SimpleRouter()

router.register(r'races', RaceViewSet)
router.register(r'race-titles', RaceTitleViewSet)
router.register(r'race-results', RaceResultViewSet)
router.register(r'race-data', ComputedRaceDataViewSet)
