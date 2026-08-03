

from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from shops.models import Shop
from categories.models import Category


class Product(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Магазин",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Категория",
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Скидка (%)",
    )
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def final_price(self):
        if self.discount_percent:
            return round(self.price * (100 - self.discount_percent) / 100, 2)
        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Товар",
    )
    image = models.ImageField(upload_to='products/%Y/%m/', verbose_name="Фото")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Фото товара"
        ordering = ['order']

    def __str__(self):
        return f"Фото для {self.product.name}"