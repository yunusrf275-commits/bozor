

from django.contrib import admin
from .models import Listing, ListingImage


class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'location', 'price', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'phone')
    autocomplete_fields = ('user', 'category', 'location')
    inlines = [ListingImageInline]
