

from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'shop', 'category', 'price', 'discount_percent', 'stock_quantity', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name',)
    autocomplete_fields = ('shop', 'category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]