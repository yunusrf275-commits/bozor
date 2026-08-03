

from .models import Category


def top_categories(request):
    return {
        'navbar_categories': Category.objects.filter(parent__isnull=True).order_by('name')
    }