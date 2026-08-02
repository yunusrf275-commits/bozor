

from django.core.management.base import BaseCommand
from locations.models import Location


class Command(BaseCommand):
    help = "Добавляет по одному тестовому селу (level=3) каждому туману (level=2)"

    def handle(self, *args, **options):
        tumans = Location.objects.filter(level=2)
        created = 0

        for tuman in tumans:
            village_name = f"{tuman.name}1"
            village, is_created = Location.objects.get_or_create(
                name=village_name,
                level=3,
                parent=tuman,
            )
            if is_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: создано {created} тестовых сёл для {tumans.count()} туманов"
        ))