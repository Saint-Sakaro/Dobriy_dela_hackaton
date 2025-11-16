from rest_framework import serializers

from locations.models import City
from locations.serializers import CitySerializer

from .models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True, allow_null=True, required=False
    )
    cover_file_url = serializers.SerializerMethodField()

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
            "cover_file",
            "cover_file_url",
            "attachment_url",
            "published_at",
            "is_published",
            "is_featured",
        ]
        read_only_fields = ("slug", "cover_file_url")

    def get_cover_file_url(self, obj):
        if obj.cover_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_file.url)
            return obj.cover_file.url
        return None
