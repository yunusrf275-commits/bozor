
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from locations.models import Location

class Shop(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название магазина")
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='shops',
        verbose_name="Локация",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='owned_shops',
        verbose_name="Владелец",
        null=True,
        blank=True,
    )
    logo = models.ImageField(upload_to='shops/logos/%Y/%m/', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    # save() и Meta без изменений — оставляем как есть

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Shop.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)

    @property
    def reviews_count(self):
        return self.reviews.count()

class ShopStaff(models.Model):
    ROLE_MANAGER = 'manager'
    ROLE_PRODUCT_MANAGER = 'product_manager'
    ROLE_ORDER_HANDLER = 'order_handler'
    ROLE_VIEWER = 'viewer'

    ROLE_CHOICES = [
        (ROLE_MANAGER, 'Управляющий (полный доступ)'),
        (ROLE_PRODUCT_MANAGER, 'Менеджер товаров'),
        (ROLE_ORDER_HANDLER, 'Продавец (приём заказов)'),
        (ROLE_VIEWER, 'Наблюдатель'),
    ]

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='staff',
        verbose_name="Магазин",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shop_staff_roles',
        verbose_name="Сотрудник",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_VIEWER,
        verbose_name="Уровень доступа",
    )

    class Meta:
        verbose_name = "Сотрудник магазина"
        verbose_name_plural = "Сотрудники магазина"
        unique_together = ('shop', 'user')

    def __str__(self):
        return f"{self.user.username} — {self.shop.name} ({self.get_role_display()})"


