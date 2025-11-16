from django.conf import settings
from django.db import models
from django.utils.text import slugify

from common.models import TimeStampedModel


class Organization(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PENDING = "pending", "На модерации"
        PUBLISHED = "published", "Опубликовано"
        REJECTED = "rejected", "Отклонено"

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.PROTECT,
        related_name="organizations",
    )
    categories = models.ManyToManyField(
        "locations.ActivityCategory",
        related_name="organizations",
        blank=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="owned_organizations",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    website = models.URLField(blank=True)
    vk_link = models.URLField(blank=True)
    telegram_link = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)
    logo_file = models.ImageField(upload_to="organizations/logos/", blank=True, null=True)
    cover_image = models.URLField(blank=True)
    cover_file = models.FileField(upload_to="organizations/covers/", blank=True, null=True, help_text="Может быть изображение или видео")
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "НКО"
        verbose_name_plural = "НКО"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Organization.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
