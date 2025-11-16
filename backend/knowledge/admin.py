from django.contrib import admin

from .models import Material, MaterialCategory


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "city", "is_published", "updated_at")
    search_fields = ("title", "summary")
    list_filter = ("type", "is_published", "city", "categories")
    autocomplete_fields = ("categories", "city", "created_by")
