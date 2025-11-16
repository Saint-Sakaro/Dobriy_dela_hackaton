from django.contrib import admin

from .models import ActivityCategory, City


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region", "is_active")
    search_fields = ("name", "region")
    list_filter = ("is_active",)


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name",)
