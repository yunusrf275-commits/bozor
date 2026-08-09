


from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shop', 'customer_phone', 'status', 'created_at')
    list_filter = ('status', 'shop')
    search_fields = ('customer_phone',)
    inlines = [OrderItemInline]