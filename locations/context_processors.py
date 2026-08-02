

from .models import Location


def regions(request):
    return {
        'navbar_regions': Location.objects.filter(level=1).order_by('name')
    }
