from django.contrib import admin

from .models import AssistantMessage, AssistantSession


class AssistantMessageInline(admin.TabularInline):
    model = AssistantMessage
    extra = 0
    readonly_fields = ("role", "content", "created_at", "tokens", "latency_ms", "sources")


@admin.register(AssistantSession)
class AssistantSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "context_type", "context_id", "last_activity")
    search_fields = ("user__username", "context_id")
    inlines = [AssistantMessageInline]
