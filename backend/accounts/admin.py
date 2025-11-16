from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Favorite, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("role", "city", "phone")}),
    )
    list_display = ("username", "email", "role", "city", "is_active", "is_staff")
    list_filter = ("role", "city", "is_staff", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", "created_at")
    search_fields = ("user__username",)
