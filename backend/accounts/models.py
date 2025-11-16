from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        RESIDENT = "resident", "Житель"
        VOLUNTEER = "volunteer", "Волонтёр"
        NKO_OWNER = "nko_owner", "Представитель НКО"
        MODERATOR = "moderator", "Модератор"
        ADMIN = "admin", "Администратор"

    role = models.CharField(
        max_length=32,
        choices=Role.choices,
        default=Role.RESIDENT,
    )
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    phone = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    @property
    def is_nko_owner(self):
        return self.role == self.Role.NKO_OWNER

    @property
    def is_moderator(self):
        return self.role in {self.Role.MODERATOR, self.Role.ADMIN}

    def __str__(self) -> str:
        return self.get_full_name() or self.username


class Favorite(TimeStampedModel):
    ALLOWED_MODELS = ("organization", "event", "material", "newsitem")

    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        unique_together = ("user", "content_type", "object_id")
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def clean(self):
        if self.content_type.model not in self.ALLOWED_MODELS:
            raise ValueError("Недопустимый тип для избранного.")

    def __str__(self) -> str:
        return f"{self.user} -> {self.content_type}#{self.object_id}"
