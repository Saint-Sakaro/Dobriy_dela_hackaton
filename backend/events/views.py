from django.db import models
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from common.permissions import IsOwnerOrModerator
from .models import Event, EventRegistration
from .serializers import EventRegistrationSerializer, EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        qs = Event.objects.all()
        if self.action in {"list", "retrieve"} and not self.request.user.is_authenticated:
            qs = qs.filter(status=Event.EventStatus.PUBLISHED)
        elif self.action in {"list", "retrieve"} and self.request.user.is_authenticated and not self.request.user.is_moderator:
            qs = qs.filter(
                models.Q(status=Event.EventStatus.PUBLISHED)
                | models.Q(organization__owner=self.request.user)
                | models.Q(created_by=self.request.user)
            )
        city = self.request.query_params.get("city")
        if city:
            qs = qs.filter(city__slug=city)
        featured = self.request.query_params.get("featured")
        if featured:
            qs = qs.filter(is_featured=True)
        category = self.request.query_params.get("category")
        if category:
            qs = qs.filter(categories__id=category)
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        search = self.request.query_params.get("search")
        if search:
            qs = qs.filter(title__icontains=search)
        return qs.select_related("city", "organization").prefetch_related("categories")

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsOwnerOrModerator()]
        if self.action in ["register", "cancel_registration", "my_registrations"]:
            return [permissions.IsAuthenticated()]
        if self.action == "moderate":
            return [IsOwnerOrModerator()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(status=Event.EventStatus.DRAFT, created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def register(self, request, pk=None):
        event = self.get_object()
        registration, _ = EventRegistration.objects.get_or_create(event=event, user=request.user)
        registration.status = EventRegistration.RegistrationStatus.REGISTERED
        registration.save(update_fields=["status"])
        return Response({"status": registration.status})

    @action(detail=True, methods=["post"])
    def cancel_registration(self, request, pk=None):
        event = self.get_object()
        try:
            registration = EventRegistration.objects.get(event=event, user=request.user)
        except EventRegistration.DoesNotExist:
            return Response({"detail": "Регистрация не найдена."}, status=status.HTTP_404_NOT_FOUND)
        registration.status = EventRegistration.RegistrationStatus.CANCELLED
        registration.save(update_fields=["status"])
        return Response({"status": registration.status})

    @action(detail=False, methods=["get"])
    def my_registrations(self, request):
        registrations = EventRegistration.objects.filter(user=request.user)
        serializer = EventRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def moderate(self, request, pk=None):
        if not request.user.is_moderator:
            return Response(status=status.HTTP_403_FORBIDDEN)
        event = self.get_object()
        action_type = request.data.get("action")
        if action_type == "approve":
            event.status = Event.EventStatus.PUBLISHED
        elif action_type == "reject":
            event.status = Event.EventStatus.ARCHIVED
        else:
            return Response({"detail": "Некорректное действие."}, status=status.HTTP_400_BAD_REQUEST)
        event.save(update_fields=["status"])
        return Response({"status": event.status})
