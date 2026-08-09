

import random
from django.core.management.base import BaseCommand
from shops.models import Shop
from categories.models import Category
from products.models import Product


class Command(BaseCommand):
    help = "Создаёт по 2 тестовых товара в разных категориях для каждого магазина"

    def handle(self, *args, **options):
        shops = Shop.objects.all()
        # берём только листовые категории (подкатегории, без своих детей) — товары логичнее привязывать к ним
        categories = list(Category.objects.filter(children__isnull=True))

        if not categories:
            self.stdout.write(self.style.ERROR('Нет категорий. Сначала запустите load_categories.'))
            return

        created = 0

        for shop in shops:
            chosen_categories = random.sample(categories, min(2, len(categories)))
            for i, category in enumerate(chosen_categories, start=1):
                name = f"{category.name} — товар {shop.id}-{i}"
                product, is_created = Product.objects.get_or_create(
                    shop=shop,
                    name=name,
                    defaults={
                        'category': category,
                        'price': random.randint(10000, 500000),
                        'discount_percent': random.choice([0, 0, 0, 10, 15, 20]),
                        'stock_quantity': random.randint(1, 50),
                    },
                )
                if is_created:
                    created += 1

        self.stdout.write(self.style.SUCCESS(f"Готово: создано {created} тестовых товаров"))