

from django.conf import settings
from django.db import models
from shops.models import Shop
from products.models import Product


class FavoriteShop(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_shops')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'shop')
        verbose_name = "Избранный магазин"
        verbose_name_plural = "Избранные магазины"

    def __str__(self):
        return f"{self.user.username} — {self.shop.name}"


class FavoriteProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorite_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        verbose_name = "Избранный товар"
        verbose_name_plural = "Избранные товары"

    def __str__(self):
        return f"{self.user.username} — {self.product.name}"
