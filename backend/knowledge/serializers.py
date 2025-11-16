from rest_framework import serializers

from locations.models import City
from locations.serializers import CitySerializer

from .models import Material, MaterialCategory


class MaterialCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialCategory
        fields = ("id", "name", "description")


class MaterialSerializer(serializers.ModelSerializer):
    categories = MaterialCategorySerializer(many=True, read_only=True)
    city = CitySerializer(read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=MaterialCategory.objects.all(), source="categories", many=True, write_only=True, required=False
    )
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Material
        fields = [
            "id",
            "title",
            "summary",
            "body",
            "file_url",
            "cover_image",
            "type",
            "categories",
            "category_ids",
            "city",
            "city_id",
            "is_published",
            "updated_at",
        ]
        read_only_fields = ("updated_at",)
