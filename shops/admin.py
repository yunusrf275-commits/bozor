

from django.contrib import admin
from .models import Shop
from .models import Shop, ShopStaff


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'owner', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    autocomplete_fields = ('location', 'owner')
    prepopulated_fields = {'slug': ('name',)}



@admin.register(ShopStaff)
class ShopStaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'shop', 'role')
    list_filter = ('role', 'shop')
    autocomplete_fields = ('shop', 'user')