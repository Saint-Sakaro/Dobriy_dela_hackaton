from django.db import migrations

CITIES = [
    ("Ангарск", "Иркутская область", "angarsk"),
    ("Байкальск", "Иркутская область", "baikalsk"),
    ("Балаково", "Саратовская область", "balakovo"),
    ("Билибино", "Чукотский АО", "bilibino"),
    ("Волгодонск", "Ростовская область", "volgodonsk"),
    ("Глазов", "Удмуртская Республика", "glazov"),
    ("Десногорск", "Смоленская область", "desnogorsk"),
    ("Димитровград", "Ульяновская область", "dimitrovgrad"),
    ("Железногорск", "Красноярский край", "zheleznogirsk"),
    ("ЗАТО Заречный", "Пензенская область", "zarechny-penza"),
    ("Заречный", "Свердловская область", "zarechny"),
    ("Зеленогорск", "Красноярский край", "zelenogorsk"),
    ("Краснокаменск", "Забайкальский край", "krasnokamensk"),
    ("Курчатов", "Курская область", "kurchatov"),
    ("Лесной", "Свердловская область", "lesnoy"),
    ("Неман", "Калининградская область", "neman"),
    ("Нововоронеж", "Воронежская область", "novovoronezh"),
    ("Новоуральск", "Свердловская область", "novouralsk"),
    ("Обнинск", "Калужская область", "obninsk"),
    ("Озерск", "Челябинская область", "ozersk"),
    ("Певек", "Чукотский АО", "pevek"),
    ("Полярные Зори", "Мурманская область", "polyarnye-zori"),
    ("Саров", "Нижегородская область", "sarov"),
    ("Северск", "Томская область", "seversk"),
    ("Снежинск", "Челябинская область", "snezhinsk"),
    ("Советск", "Калининградская область", "sovetsk"),
    ("Сосновый Бор", "Ленинградская область", "sosnovy-bor"),
    ("Трехгорный", "Челябинская область", "trekhgorny"),
    ("Удомля", "Тверская область", "udomlya"),
    ("Усолье-Сибирское", "Иркутская область", "usolye-sibirskoye"),
    ("Электросталь", "Московская область", "electrostal"),
    ("Энергодар", "Запорожская область", "energodar"),
]

ACTIVITY_CATEGORIES = [
    ("Экология", "Природоохранные инициативы, озеленение, раздельный сбор"),
    ("Культура", "Культурные проекты, музеи, творческие мастерские"),
    ("Спорт", "ЗОЖ, спортивные мероприятия"),
    ("Социальная помощь", "Поддержка людей, благотворительные акции"),
    ("Образование", "Обучение, просветительские программы"),
]


def seed_data(apps, schema_editor):
    City = apps.get_model("locations", "City")
    ActivityCategory = apps.get_model("locations", "ActivityCategory")
    for name, region, slug in CITIES:
        City.objects.update_or_create(slug=slug, defaults={"name": name, "region": region})
    for name, description in ACTIVITY_CATEGORIES:
        ActivityCategory.objects.update_or_create(name=name, defaults={"description": description})


def unseed_data(apps, schema_editor):
    City = apps.get_model("locations", "City")
    ActivityCategory = apps.get_model("locations", "ActivityCategory")
    City.objects.filter(slug__in=[slug for _, _, slug in CITIES]).delete()
    ActivityCategory.objects.filter(name__in=[name for name, _ in ACTIVITY_CATEGORIES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("locations", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]

