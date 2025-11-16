from django.db import models
from django.utils.text import slugify


class City(models.Model):
    name = models.CharField(max_length=128, unique=True)
    region = models.CharField(max_length=128, blank=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class ActivityCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=64, blank=True, help_text="Например, имя иконки из UI-кита.")

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория активности"
        verbose_name_plural = "Категории активностей"

    def __str__(self) -> str:
        return self.name
