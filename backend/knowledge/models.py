from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class MaterialCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория материала"
        verbose_name_plural = "Категории материалов"

    def __str__(self) -> str:
        return self.name


class Material(TimeStampedModel):
    class MaterialType(models.TextChoices):
        ARTICLE = "article", "Статья"
        VIDEO = "video", "Видео"
        DOCUMENT = "document", "Документ"
        LINK = "link", "Ссылка"

    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True)
    body = models.TextField(blank=True)
    file_url = models.URLField(blank=True)
    cover_image = models.URLField(blank=True)
    cover_file = models.FileField(upload_to="materials/covers/", blank=True, null=True, help_text="Может быть изображение или видео")
    type = models.CharField(
        max_length=32, choices=MaterialType.choices, default=MaterialType.ARTICLE
    )
    categories = models.ManyToManyField(
        MaterialCategory,
        related_name="materials",
        blank=True,
    )
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materials",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materials",
    )
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self) -> str:
        return self.title
