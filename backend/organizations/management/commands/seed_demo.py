from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from events.models import Event
from knowledge.models import Material, MaterialCategory
from locations.models import ActivityCategory, City
from news.models import NewsItem
from organizations.models import Organization


class Command(BaseCommand):
    help = "Seed demo data for local development"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data…")

        city_sarov = City.objects.filter(slug="sarov").first()
        city_obninsk = City.objects.filter(slug="obninsk").first()
        if not city_sarov or not city_obninsk:
            self.stderr.write("Города еще не загружены. Выполните миграции locations.")
            return

        eco_category = ActivityCategory.objects.filter(name="Экология").first()
        culture_category = ActivityCategory.objects.filter(name="Культура").first()

        owner, _ = User.objects.get_or_create(
            username="demo_owner",
            defaults={"email": "owner@example.com", "role": User.Role.NKO_OWNER},
        )
        owner.set_password("demo12345")
        owner.save()

        moderator, _ = User.objects.get_or_create(
            username="demo_moderator",
            defaults={"email": "moderator@example.com", "role": User.Role.MODERATOR},
        )
        moderator.set_password("demo12345")
        moderator.save()

        org, _ = Organization.objects.update_or_create(
            slug="eco-green-world",
            defaults={
                "name": "Экологический центр «Зелёный мир»",
                "tagline": "Сохраняем природу вместе",
                "description": "Организация проводит экологические акции, субботники и образовательные занятия.",
                "city": city_sarov,
                "owner": owner,
                "status": Organization.Status.PUBLISHED,
                "email": "eco@example.com",
            },
        )
        if eco_category:
            org.categories.set([eco_category])

        event, _ = Event.objects.update_or_create(
            title="Экологический субботник",
            city=city_sarov,
            defaults={
                "description": "Собираемся в городском парке и наводим порядок.",
                "organization": org,
                "start_at": timezone.now() + timezone.timedelta(days=7),
                "end_at": timezone.now() + timezone.timedelta(days=7, hours=3),
                "venue": "Городской парк",
                "status": Event.EventStatus.PUBLISHED,
                "created_by": owner,
            },
        )
        if eco_category:
            event.categories.set([eco_category])

        material_category, _ = MaterialCategory.objects.get_or_create(name="Методики")
        material, _ = Material.objects.update_or_create(
            title="Как провести экологическую акцию",
            defaults={
                "summary": "Пошаговое руководство для координаторов.",
                "body": "1. Соберите команду\n2. Выберите локацию\n3. Подготовьте инвентарь",
                "type": Material.MaterialType.ARTICLE,
                "city": city_sarov,
                "is_published": True,
                "created_by": moderator,
            },
        )
        material.categories.set([material_category])

        NewsItem.objects.update_or_create(
            title="Запущен портал «Добрые дела Росатома»",
            defaults={
                "excerpt": "Единая платформа для жителей, НКО и волонтеров.",
                "content": "Сегодня мы запустили портал «Добрые дела Росатома» для всех городов присутствия.",
                "city": city_obninsk,
                "is_published": True,
                "published_at": timezone.now(),
                "author": moderator,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data ready."))

