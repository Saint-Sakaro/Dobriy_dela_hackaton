from django.db import models
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsOwnerOrModerator
from .models import Organization
from .serializers import OrganizationSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def get_queryset(self):
        qs = Organization.objects.all()
        mine = self.request.query_params.get("mine")
        if mine and self.request.user.is_authenticated:
            qs = qs.filter(owner=self.request.user)
        elif self.action in {"list", "retrieve"} and not self.request.user.is_authenticated:
            qs = qs.filter(status=Organization.Status.PUBLISHED)
        elif self.action in {"list", "retrieve"} and self.request.user.is_authenticated and not self.request.user.is_moderator:
            qs = qs.filter(
                models.Q(status=Organization.Status.PUBLISHED)
                | models.Q(owner=self.request.user)
            )

        city = self.request.query_params.get("city")
        if city:
            qs = qs.filter(city__slug=city)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(categories__id=category)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search)
        featured = self.request.query_params.get("featured")
        if featured:
            qs = qs.filter(is_featured=True)
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs.select_related("city", "owner").prefetch_related("categories")

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy", "submit"]:
            return [permissions.IsAuthenticated(), IsOwnerOrModerator()]
        if self.action == "moderate":
            return [IsOwnerOrModerator()]
        return super().get_permissions()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        # При создании НКО сразу отправляем на модерацию
        serializer.save(owner=self.request.user, status=Organization.Status.PENDING)

    @action(detail=True, methods=["post"])
    def submit(self, request, slug=None):
        org = self.get_object()
        if org.owner != request.user:
            return Response({"detail": "Можно отправить только свою организацию."}, status=status.HTTP_403_FORBIDDEN)
        org.status = Organization.Status.PENDING
        org.save(update_fields=["status"])
        return Response({"status": org.status})

    @action(detail=True, methods=["post"])
    def moderate(self, request, slug=None):
        org = self.get_object()
        if not request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        action_type = request.data.get("action")
        if action_type == "approve":
            org.status = Organization.Status.PUBLISHED
        elif action_type == "reject":
            org.status = Organization.Status.REJECTED
        else:
            return Response({"detail": "Некорректное действие."}, status=status.HTTP_400_BAD_REQUEST)
        org.save(update_fields=["status"])
        return Response({"status": org.status})
