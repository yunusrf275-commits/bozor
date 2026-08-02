

from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    autocomplete_fields = ('location', 'owner')
    prepopulated_fields = {'slug': ('name',)}
