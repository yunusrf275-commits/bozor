


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

class SellerApplication(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_CONTACTED, 'Связались'),
        (STATUS_APPROVED, 'Одобрена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    name = models.CharField(max_length=100, verbose_name="Имя заявителя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заявки")

    class Meta:
        verbose_name = "Заявка на открытие магазина"
        verbose_name_plural = "Заявки на открытие магазина"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.phone}"
