from django.db import models

from common.models import TimeStampedModel


class Event(TimeStampedModel):
    class EventStatus(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PENDING = "pending", "На модерации"
        PUBLISHED = "published", "Опубликовано"
        ARCHIVED = "archived", "Архив"

    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        related_name="events",
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    created_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_events",
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    venue = models.CharField(max_length=255, blank=True)
    registration_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=EventStatus.choices,
        default=EventStatus.DRAFT,
    )
    categories = models.ManyToManyField(
        "locations.ActivityCategory",
        related_name="events",
        blank=True,
    )
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["start_at"]
        verbose_name = "Событие"
        verbose_name_plural = "События"

    def __str__(self) -> str:
        return self.title


class EventRegistration(TimeStampedModel):
    class RegistrationStatus(models.TextChoices):
        REGISTERED = "registered", "Зарегистрирован"
        CANCELLED = "cancelled", "Отменён"

    event = models.ForeignKey(Event, related_name="registrations", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", related_name="event_registrations", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=RegistrationStatus.choices, default=RegistrationStatus.REGISTERED)

    class Meta:
        unique_together = ("event", "user")
        verbose_name = "Регистрация на событие"
        verbose_name_plural = "Регистрации на события"

    def __str__(self) -> str:
        return f"{self.user} -> {self.event}"
