from rest_framework.response import Response
from rest_framework import viewsets

from ironman_stats.main.models import Race, RaceResult, ComputedRaceData
from .serializers import (RaceSerializer, RaceResultSerializer,
                          RaceTitleSerializer, ComputedRaceDataSerializer)


class RaceTitleViewSet(viewsets.ViewSet):
    queryset = Race.objects.all()

    def list(self, request):
        distance = request.query_params.get('distance', None)
        if distance is not None:
            queryset = self.queryset.filter(distance=distance)
        else:
            queryset = self.queryset

        queryset = queryset.values('title', 'distance', 'location').order_by('location').distinct()
        serializer = RaceTitleSerializer(queryset, many=True)
        return Response(serializer.data)


class RaceViewSet(viewsets.ModelViewSet):
    serializer_class = RaceSerializer
    queryset = Race.objects.all()


class RaceResultViewSet(viewsets.ModelViewSet):
    serializer_class = RaceResultSerializer
    queryset = RaceResult.objects.all()


class ComputedRaceDataViewSet(viewsets.ModelViewSet):
    serializer_class = ComputedRaceDataSerializer
    queryset = ComputedRaceData.objects.all()


"""
Calculations (for later)

################################################################
  Aggregation of a DurationField on the ComputetRaceData model:
################################################################
from django.db.models import DurationField
from django.db.models.expressions import ExpressionWrapper
result = computed_race_result_qs.aggregate(
    result=ExpressionWrapper(Avg('average_swim_time'), output_field=DurationField()))

################################################################
  Average finish time per race (per year):
################################################################
from django.db.models import DurationField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.aggregates import Avg
races = Race.objects.filter(distance='full-ironman')
finish_times = []
for race in races:
    expression = ExpressionWrapper(Avg('average_finish_time'), output_field=DurationField())
    result = (race.computedracedata_set
              .filter(average_finish_time__isnull=False)
              .aggregate(result=expression)['result'])
    if result:
        finish_times.append({'race': race, 'avg_finish_time': result})
finish_times = sorted(finish_times, key=lambda k: k['avg_finish_time'], reverse=True)
for time in finish_times:
    print(time['race'], time['avg_finish_time'])

################################################################
  Average finish time per race all time:
################################################################
from django.db.models import DurationField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.aggregates import Avg
race_data = ComputedRaceData.objects.filter(race__distance='half-ironman',
                                            average_finish_time__isnull=False)
expression = ExpressionWrapper(Avg('average_finish_time'), output_field=DurationField())
result = (race_data
          .values('race__title')
          .annotate(avg_finish_time=expression)
          .order_by('race__title'))
finish_times = sorted(result, key=lambda k: k['avg_finish_time'], reverse=True)
for time in finish_times:
    print(time['race__title'], time['avg_finish_time'])

################################################################
  Average finish for individual race:
################################################################
import datetime
from django.db.models import DurationField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.aggregates import Avg
expression = ExpressionWrapper(Avg('average_finish_time'), output_field=DurationField())
race = Race.objects.get(id=12)
result = race.computedracedata_set.aggregate(result=expression)['result']
print(race, result)

##################################################
  DNF Rate for each race (per year):
##################################################
dnf_list = []
for race in Race.objects.filter(distance='full-ironman'):
    results = race.raceresult_set.all()
    registered = results.count()
    dnf = results.filter(race_status='DNF').count()
    dns = results.filter(race_status='DNS').count()
    finished = results.filter(race_status='Finished').count()
    try:
        dnf_percentage = (dnf/(registered-dns))*100
    except:
        continue  # malformed data for this race. Move along
    dnf_list.append({'race': race,
                     'dnf_percentage': dnf_percentage,
                     'dnf': dnf,
                     'dns': dns,
                     'finished': finished,
                     'registered': results.count()})
dnf_list = sorted(dnf_list, key=lambda k: k['dnf_percentage'])

##################################################
  DNF Rate for individual race:
##################################################
race = Race.objects.get(id=644)
results = race.raceresult_set.all()
registered = results.count()
dnf = results.filter(race_status='DNF').count()
dns = results.filter(race_status='DNS').count()
finished = results.filter(race_status='Finished').count()
dnf_percentage = (dnf/(registered-dns))*100
dnf_data = {'race': race,
           'dnf_percentage': dnf_percentage,
           'dnf': dnf,
           'dns': dns,
           'finished': finished,
           'registered': results.count()}

##################################################
  Average DNF rate for each race
##################################################
from django.db.models import IntegerField, Case, When, Count
queryset = RaceResult.objects.filter(race__distance='full-ironman')
queryset = queryset.values('race__title').annotate(
    dnf=Count(
        Case(When(race_status='DNF', then=1),
             output_field=IntegerField())
    ),
    dns=Count(
        Case(When(race_status='DNS', then=1),
             output_field=IntegerField())
    ),
    finished=Count(
        Case(When(race_status='Finished', then=1),
             output_field=IntegerField())
    )
).order_by('race__title')
dnf_list = sorted(queryset, key=lambda k: k['dnf']/k['finished'], reverse=True)
for dnf in dnf_list:
    print((dnf['dnf']/(dnf['finished'] + dnf['dnf']))*100, dnf['race__title'])
"""
