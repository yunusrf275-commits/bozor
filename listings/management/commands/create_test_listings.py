

import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from locations.models import Location
from categories.models import Category
from listings.models import Listing

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт 100 тестовых покупателей и по 2 объявления каждому в разных категориях"

    def handle(self, *args, **options):
        categories = list(Category.objects.filter(children__isnull=True))
        locations = list(Location.objects.filter(level__in=[2, 3]))

        if not categories:
            self.stdout.write(self.style.ERROR('Нет категорий. Сначала запустите load_categories.'))
            return
        if not locations:
            self.stdout.write(self.style.ERROR('Нет locations. Сначала запустите load_locations.'))
            return

        created_users = 0
        created_listings = 0

        for i in range(1, 101):
            username = f"test_customer_{i}"
            user, is_created = User.objects.get_or_create(
                username=username,
                defaults={'role': User.ROLE_CUSTOMER, 'phone': f'+99890{1000000 + i}'},
            )
            if is_created:
                user.set_password('testpass123')
                user.save()
                created_users += 1

            chosen_categories = random.sample(categories, min(2, len(categories)))
            for j, category in enumerate(chosen_categories, start=1):
                location = random.choice(locations)
                listing, is_created = Listing.objects.get_or_create(
                    user=user,
                    title=f"{category.name} — объявление {i}-{j}",
                    defaults={
                        'description': 'Тестовое объявление',
                        'price': random.randint(10000, 2000000),
                        'category': category,
                        'location': location,
                        'phone': user.phone,
                        'status': Listing.STATUS_APPROVED,
                    },
                )
                if is_created:
                    created_listings += 1

        self.stdout.write(self.style.SUCCESS(
            f"Готово: создано {created_users} пользователей и {created_listings} объявлений"
        ))