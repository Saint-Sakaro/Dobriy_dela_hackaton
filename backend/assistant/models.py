from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class AssistantSession(TimeStampedModel):
    CONTEXT_CHOICES = [
        ("nko", "НКО"),
        ("event", "Событие"),
        ("material", "Материал"),
        ("news", "Новость"),
        ("general", "Общий вопрос"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assistant_sessions",
    )
    context_type = models.CharField(max_length=32, choices=CONTEXT_CHOICES, default="general")
    context_id = models.CharField(max_length=64, blank=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Сессия помощника"
        verbose_name_plural = "Сессии помощника"

    def __str__(self) -> str:
        return f"{self.user} ({self.context_type})"


class AssistantMessage(TimeStampedModel):
    class Role(models.TextChoices):
        USER = "user", "Пользователь"
        ASSISTANT = "assistant", "Ассистент"
        SYSTEM = "system", "Система"

    session = models.ForeignKey(
        AssistantSession,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    role = models.CharField(max_length=32, choices=Role.choices)
    content = models.TextField()
    tokens = models.PositiveIntegerField(default=0)
    sources = models.JSONField(blank=True, default=list)
    latency_ms = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Сообщение ассистента"
        verbose_name_plural = "Сообщения ассистента"

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:40]}"
