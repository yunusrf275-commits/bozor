

from django.contrib import admin
from .models import Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'show_in_footer', 'order')
    list_filter = ('is_published', 'show_in_footer')
    prepopulated_fields = {'slug': ('title',)}
