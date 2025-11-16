from django.db import models
from rest_framework import permissions, viewsets

from common.permissions import IsModerator
from .models import Material, MaterialCategory
from .serializers import MaterialCategorySerializer, MaterialSerializer


class MaterialCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaterialCategory.objects.all()
    serializer_class = MaterialCategorySerializer
    permission_classes = [permissions.AllowAny]


class MaterialViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        qs = Material.objects.all()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_published=True)
        elif not self.request.user.is_moderator:
            qs = qs.filter(models.Q(is_published=True) | models.Q(created_by=self.request.user))
        city = self.request.query_params.get("city")
        if city:
            qs = qs.filter(city__slug=city)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(categories__id=category)
        return qs.select_related("city", "created_by").prefetch_related("categories")

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsModerator()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
