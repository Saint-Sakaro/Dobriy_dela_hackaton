from django.conf import settings
from django.db import models
from django.utils.text import slugify

from common.models import TimeStampedModel


class NewsItem(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True)
    category = models.CharField(max_length=100, blank=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    city = models.ForeignKey(
        "locations.City",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
    )
    cover_image = models.URLField(blank=True)
    attachment_url = models.URLField(blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news_items",
    )
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:250]
            slug = base_slug
            index = 1
            while type(self).objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{index}"
                index += 1
            self.slug = slug
        super().save(*args, **kwargs)
