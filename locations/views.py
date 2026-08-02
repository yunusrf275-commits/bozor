
from django.http import JsonResponse
from .models import Location


def get_children(request):
    parent_id = request.GET.get('parent_id')
    children = Location.objects.filter(parent_id=parent_id).order_by('name').values('id', 'name')
    return JsonResponse(list(children), safe=False)