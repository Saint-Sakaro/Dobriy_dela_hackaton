from rest_framework import serializers

from .models import ActivityCategory, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "region", "slug")


class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ("id", "name", "description", "icon")

