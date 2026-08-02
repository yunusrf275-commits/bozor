


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CUSTOMER = 'customer'
    ROLE_SHOP_OWNER = 'shop_owner'

    ROLE_CHOICES = [
        (ROLE_CUSTOMER, 'Покупатель'),
        (ROLE_SHOP_OWNER, 'Владелец магазина'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_CUSTOMER,
        verbose_name="Роль",
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
