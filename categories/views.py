

from django.http import JsonResponse
from .models import Category


def get_children(request):
    parent_id = request.GET.get('parent_id')
    children = Category.objects.filter(parent_id=parent_id).order_by('name').values('id', 'name')
    return JsonResponse(list(children), safe=False)
