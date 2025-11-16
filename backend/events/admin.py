from django.contrib import admin

from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "start_at", "end_at", "status", "is_featured")
    list_filter = ("status", "city", "categories")
    search_fields = ("title", "description", "venue")
    autocomplete_fields = ("city", "organization", "categories")


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("event__title", "user__username")
