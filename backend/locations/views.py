from rest_framework import permissions, viewsets

from .models import ActivityCategory, City
from .serializers import ActivityCategorySerializer, CitySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "slug"


class ActivityCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityCategory.objects.all()
    serializer_class = ActivityCategorySerializer
    permission_classes = [permissions.AllowAny]
