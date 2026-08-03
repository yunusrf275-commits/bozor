

from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    autocomplete_fields = ('parent',)
    prepopulated_fields = {'slug': ('name',)}
