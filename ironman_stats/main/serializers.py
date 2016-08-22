from rest_framework import serializers
from ironman_stats.main.models import Race, RaceResult, ComputedRaceData


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race


class RaceResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult


class RaceTitleSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    distance_slug = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    def get_distance(self, obj):
        return Race.DISTANCES[obj['distance']]

    def get_distance_slug(self, obj):
        return obj['distance']


class ComputedRaceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComputedRaceData
