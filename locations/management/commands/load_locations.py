

import json
from django.core.management.base import BaseCommand
from locations.models import Location
from django.conf import settings


class Command(BaseCommand):
    help = "Загружает вилояты и туманы из JSON-файла"

    def handle(self, *args, **options):

        file_path = settings.BASE_DIR / "fixtures" / "viloyat_tuman.json"
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        created_viloyat = 0
        created_tuman = 0

        for viloyat_data in data:
            viloyat, created = Location.objects.get_or_create(
                name=viloyat_data["name"],
                level=1,
                parent=None,
            )
            if created:
                created_viloyat += 1

            for tuman_name in viloyat_data["children"]:
                tuman, created = Location.objects.get_or_create(
                    name=tuman_name,
                    level=2,
                    parent=viloyat,
                )
                if created:
                    created_tuman += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: создано {created_viloyat} областей и {created_tuman} районов"
        ))