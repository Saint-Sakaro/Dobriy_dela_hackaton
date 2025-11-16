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
            "cover_image",
            "is_featured",
            "status",
            "updated_at",
        ]
        read_only_fields = ("slug", "status", "is_featured", "updated_at")
