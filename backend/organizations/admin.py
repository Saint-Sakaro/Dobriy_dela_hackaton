from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "status", "is_featured", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("status", "city", "categories")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("city", "categories", "owner")
