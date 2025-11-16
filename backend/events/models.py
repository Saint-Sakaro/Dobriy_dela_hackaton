from django.db import models
from django.utils.text import slugify

from common.models import TimeStampedModel


class Event(TimeStampedModel):
    class EventStatus(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PENDING = "pending", "На модерации"
        PUBLISHED = "published", "Опубликовано"
        ARCHIVED = "archived", "Архив"

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
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
    cover_image = models.URLField(blank=True)
    cover_file = models.ImageField(upload_to="events/covers/", blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        # Автоматически генерируем registration_url, если он не указан
        if not self.registration_url and self.slug:
            # Используем относительный URL, фронтенд добавит базовый путь
            self.registration_url = f"/calendar/event/{self.slug}"
        super().save(*args, **kwargs)

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
