"""
Импорт НКО из CSV файла (экспортированного из Google таблицы).

Использование:
1. Экспортируйте Google таблицу в CSV (File -> Download -> Comma-separated values)
2. Сохраните файл как backend/organizations_data.csv
3. Запустите: python manage.py import_ngo_from_csv

Формат CSV:
- Колонка B: Название организации
- Колонка C: Про организацию (описание)
- Колонка D: Ссылка на социальные сети (VK)
- Колонка A: Деятельность НКО (категория)
"""
import csv
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from locations.models import City, ActivityCategory
from organizations.models import Organization
from accounts.models import User


class Command(BaseCommand):
    help = "Импорт НКО из CSV файла"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="organizations_data.csv",
            help="Путь к CSV файлу (относительно backend/)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Показать что будет импортировано без сохранения",
        )

    def handle(self, *args, **options):
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", options["file"])
        dry_run = options["dry_run"]

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Файл не найден: {file_path}"))
            self.stdout.write(
                self.style.WARNING(
                    "Экспортируйте Google таблицу в CSV и сохраните как backend/organizations_data.csv"
                )
            )
            return

        # Маппинг городов (из Google таблицы в нашу БД)
        # Пробуем найти город по частичному совпадению названия
        def find_city_by_name(text: str) -> City | None:
            """Находит город по частичному совпадению в тексте"""
            text_lower = text.lower()
            # Список городов из миграции (соответствует backend/locations/migrations/0002_seed_cities.py)
            city_keywords = {
                "ангарск": "angarsk",
                "волгодонск": "volgodonsk",
                "глазов": "glazov",
                "железногорск": "zheleznogirsk",  # Обратите внимание: в миграции zheleznogirsk
                "зеленогорск": "zelenogorsk",
                "обнинск": "obninsk",
                "омск": "omsk",
                "северск": "seversk",
                "снежинск": "snezhinsk",
                "усолье-сибирское": "usolye-sibirskoye",  # В миграции usolye-sibirskoye
                "озёрск": "ozersk",
                "озерск": "ozersk",
                "байкальск": "baikalsk",
                "балаково": "balakovo",
                "билибино": "bilibino",
                "десногорск": "desnogorsk",
                "димитровград": "dimitrovgrad",
                "заречный": "zarechny",
                "краснокаменск": "krasnokamensk",
                "курчатов": "kurchatov",
                "лесной": "lesnoy",
                "неман": "neman",
                "нововоронеж": "novovoronezh",
                "новоуральск": "novouralsk",
                "певек": "pevek",
                "полярные зори": "polyarnye-zori",
                "саров": "sarov",
                "советск": "sovetsk",
                "сосновый бор": "sosnovy-bor",
                "трехгорный": "trekhgorny",
                "удомля": "udomlya",
                "электросталь": "electrostal",
                "энергодар": "energodar",
            }
            
            for keyword, slug in city_keywords.items():
                if keyword in text_lower:
                    return City.objects.filter(slug=slug).first()
            return None

        # Маппинг категорий
        category_mapping = {
            "Местное сообщество и развитие территорий": "Местное сообщество",
            "Местное сообщество": "Местное сообщество",
            "Экология": "Экология",
            "Культура и искусство": "Культура",
            "Культура": "Культура",
            "Образование": "Образование",
            "Спорт": "Спорт",
            "Социальная помощь": "Социальная помощь",
            "Здоровье": "Здоровье",
        }
        
        # Создаем категорию "Местное сообщество" если её нет
        ActivityCategory.objects.get_or_create(
            name="Местное сообщество",
            defaults={"description": "Развитие территорий, местные инициативы, ТОС"}
        )

        imported = 0
        skipped = 0
        errors = []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                # Пропускаем первые 2 строки (заголовки)
                reader = csv.reader(f)
                next(reader)  # Пропускаем первую строку
                next(reader)  # Пропускаем вторую строку

                with transaction.atomic():
                    for row_num, row in enumerate(reader, start=3):
                        if len(row) < 4:
                            continue

                        try:
                            # Парсинг данных
                            category_name = row[0].strip() if len(row) > 0 else ""
                            org_name = row[1].strip() if len(row) > 1 else ""
                            description = row[2].strip() if len(row) > 2 else ""
                            social_link = row[3].strip() if len(row) > 3 else ""

                            if not org_name:
                                skipped += 1
                                continue

                            # Определяем город из названия или описания
                            city = find_city_by_name(org_name) or find_city_by_name(description)
                            
                            if not city:
                                # Пробуем найти город по списку (fallback)
                                city = City.objects.filter(is_active=True).first()
                                if not city:
                                    errors.append(f"Строка {row_num}: Не удалось определить город для {org_name}")
                                    skipped += 1
                                    continue
                                self.stdout.write(
                                    self.style.WARNING(
                                        f"⚠ Город не определен для '{org_name}', используется {city.name}"
                                    )
                                )

                            # Определяем категорию
                            category = None
                            if category_name:
                                category_mapped = category_mapping.get(category_name, category_name)
                                category = ActivityCategory.objects.filter(name__icontains=category_mapped).first()
                                if not category:
                                    # Создаем категорию если не найдена
                                    category = ActivityCategory.objects.create(
                                        name=category_mapped, description=category_name
                                    )

                            # Извлекаем VK ссылку
                            vk_link = ""
                            if social_link and "vk.com" in social_link.lower():
                                vk_link = social_link if social_link.startswith("http") else f"https://{social_link}"

                            # Создаем или обновляем НКО
                            if dry_run:
                                self.stdout.write(
                                    self.style.SUCCESS(
                                        f"[DRY RUN] Будет создано: {org_name} в {city.name}"
                                    )
                                )
                                imported += 1
                            else:
                                org, created = Organization.objects.get_or_create(
                                    name=org_name,
                                    defaults={
                                        "description": description[:2000] if len(description) > 2000 else description,
                                        "tagline": description[:200] if description else "",
                                        "city": city,
                                        "status": Organization.Status.PUBLISHED,
                                        "vk_link": vk_link,
                                    },
                                )

                                if category:
                                    org.categories.add(category)

                                if created:
                                    imported += 1
                                    self.stdout.write(
                                        self.style.SUCCESS(f"✓ Создано: {org_name} в {city.name}")
                                    )
                                else:
                                    skipped += 1
                                    self.stdout.write(
                                        self.style.WARNING(f"⊘ Уже существует: {org_name}")
                                    )

                        except Exception as e:
                            errors.append(f"Строка {row_num}: {str(e)}")
                            self.stdout.write(self.style.ERROR(f"✗ Ошибка в строке {row_num}: {str(e)}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка чтения файла: {str(e)}"))
            return

        # Итоги
        self.stdout.write(self.style.SUCCESS(f"\n{'='*50}"))
        self.stdout.write(self.style.SUCCESS(f"Импортировано: {imported}"))
        self.stdout.write(self.style.WARNING(f"Пропущено: {skipped}"))
        if errors:
            self.stdout.write(self.style.ERROR(f"Ошибок: {len(errors)}"))
            for error in errors[:10]:  # Показываем первые 10 ошибок
                self.stdout.write(self.style.ERROR(f"  - {error}"))

