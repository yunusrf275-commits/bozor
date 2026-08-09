
import json
from django.conf import settings
from django.core.management.base import BaseCommand
from categories.models import Category


class Command(BaseCommand):
    help = "Загружает категории и подкатегории из JSON-файла"

    def handle(self, *args, **options):
        file_path = settings.BASE_DIR / "fixtures" / "categories.json"
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        created_parents = 0
        created_children = 0

        for category_data in data:
            parent, created = Category.objects.get_or_create(name=category_data["name"], parent=None)
            if created:
                created_parents += 1

            for child_name in category_data["children"]:
                child, created = Category.objects.get_or_create(name=child_name, parent=parent)
                if created:
                    created_children += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: создано {created_parents} категорий и {created_children} подкатегорий"
        ))