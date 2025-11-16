from django.conf import settings
from rest_framework import serializers

from locations.models import ActivityCategory, City
from locations.serializers import ActivityCategorySerializer, CitySerializer

from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    categories = ActivityCategorySerializer(many=True, read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True, required=True
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=ActivityCategory.objects.all(), source="categories", many=True, write_only=True, required=False
    )
    logo_file_url = serializers.SerializerMethodField()
    cover_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "slug",
            "tagline",
            "description",
            "city",
            "city_id",
            "categories",
            "category_ids",
            "email",
            "phone",
            "website",
            "vk_link",
            "telegram_link",
            "logo_url",
            "logo_file",
            "logo_file_url",
            "cover_image",
            "cover_file",
            "cover_file_url",
            "is_featured",
            "status",
            "updated_at",
        ]
        read_only_fields = ("slug", "status", "is_featured", "updated_at", "logo_file_url", "cover_file_url")

    def get_logo_file_url(self, obj):
        if obj.logo_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.logo_file.url)
            return obj.logo_file.url
        return None

    def get_cover_file_url(self, obj):
        if obj.cover_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_file.url)
            return obj.cover_file.url
        return None
