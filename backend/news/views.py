from rest_framework import permissions, viewsets

from common.permissions import IsModerator
from .models import NewsItem
from .serializers import NewsItemSerializer


class NewsItemViewSet(viewsets.ModelViewSet):
    serializer_class = NewsItemSerializer
    lookup_field = "slug"

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def get_queryset(self):
        qs = NewsItem.objects.all()
        if not self.request.user.is_authenticated or not self.request.user.is_moderator:
            qs = qs.filter(is_published=True)
        city = self.request.query_params.get("city")
        if city:
            qs = qs.filter(city__slug=city)
        featured = self.request.query_params.get("featured")
        if featured:
            qs = qs.filter(is_featured=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(category=category)
        return qs.select_related("city")

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [IsModerator()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
