from rest_framework import serializers

from locations.models import ActivityCategory, City
from locations.serializers import ActivityCategorySerializer, CitySerializer
from organizations.models import Organization
from organizations.serializers import OrganizationSerializer

from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    categories = ActivityCategorySerializer(many=True, read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), source="city", write_only=True, required=True
    )
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), source="organization", write_only=True, allow_null=True, required=False
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=ActivityCategory.objects.all(), source="categories", many=True, write_only=True, required=False
    )
    cover_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "city",
            "city_id",
            "organization",
            "organization_id",
            "start_at",
            "end_at",
            "venue",
            "registration_url",
            "cover_image",
            "cover_file",
            "cover_file_url",
            "status",
            "categories",
            "category_ids",
            "is_featured",
        ]
        read_only_fields = ("status", "is_featured", "slug", "registration_url", "cover_file_url")

    def get_cover_file_url(self, obj):
        if obj.cover_file:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.cover_file.url)
            return obj.cover_file.url
        return None


class EventRegistrationSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = EventRegistration
        fields = ("id", "event", "status", "created_at")

