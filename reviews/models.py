

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from shops.models import Shop
from products.models import Product
from orders.models import OrderItem


class ShopReview(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shop_reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('shop', 'user')
        ordering = ['-created_at']
        verbose_name = "Отзыв о магазине"
        verbose_name_plural = "Отзывы о магазинах"

    def __str__(self):
        return f"{self.user.username} → {self.shop.name} ({self.rating}★)"

    @property
    def is_verified_purchase(self):
        return OrderItem.objects.filter(
            order__shop=self.shop,
            order__customer=self.user,
        ).exists()


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        verbose_name = "Отзыв о товаре"
        verbose_name_plural = "Отзывы о товарах"

    def __str__(self):
        return f"{self.user.username} → {self.product.name} ({self.rating}★)"

    # @property
    # def is_verified_purchase(self):
    #     return OrderItem.objects.filter(
    #         order__customer=self.user,
    #         product=self.product,
    #     ).exists()
