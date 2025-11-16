from rest_framework import serializers

from locations.models import City
from locations.serializers import CitySerializer

from .models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = NewsItem
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "excerpt",
            "content",
            "city",
            "city_id",
            "cover_image",
            "attachment_url",
            "published_at",
            "is_published",
            "is_featured",
        ]
        read_only_fields = ("slug",)
