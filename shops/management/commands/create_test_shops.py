
from django.core.management.base import BaseCommand
from locations.models import Location
from shops.models import Shop


class Command(BaseCommand):
    help = "Создаёт по одному тестовому магазину для каждой locations уровня 2 и 3"

    def handle(self, *args, **options):
        locations = Location.objects.filter(level__in=[2, 3])
        created = 0

        for location in locations:
            shop_name = f"Do'kon {location.name}"
            shop, is_created = Shop.objects.get_or_create(
                name=shop_name,
                defaults={'location': location, 'is_active': True},
            )
            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: создано {created} тестовых магазинов"
        ))