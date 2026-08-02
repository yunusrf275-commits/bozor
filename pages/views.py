
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from shops.models import Shop
from locations.models import Location


def get_descendant_ids(location):
    ids = [location.id]
    for child in location.children.all():
        ids.append(child.id)
        ids += list(child.children.values_list('id', flat=True))
    return ids


def home(request):
    location_id = request.GET.get('location')
    page_number = request.GET.get('page', 1)

    shops_qs = Shop.objects.filter(is_active=True)

    selected_location = None
    if location_id:
        selected_location = Location.objects.filter(id=location_id).first()
        if selected_location:
            ids = get_descendant_ids(selected_location)
            shops_qs = shops_qs.filter(location_id__in=ids)

    # Ключ в сессии — свой для каждого фильтра, чтобы при смене региона рандом пересчитывался
    session_key = f"shops_order_{location_id or 'all'}"

    if session_key not in request.session:
        # Первый заход с этим фильтром — генерируем и запоминаем порядок
        ids_list = list(shops_qs.values_list('id', flat=True))
        random.shuffle(ids_list)
        request.session[session_key] = ids_list
    else:
        ids_list = request.session[session_key]

    # Django Paginator работает со списком id, сами объекты достаём отдельно
    paginator = Paginator(ids_list, 20)
    page_obj = paginator.get_page(page_number)

    # Достаём объекты магазинов в том порядке, что зафиксирован в сессии

    # Достаём объекты магазинов в том порядке, что зафиксирован в сессии
    shops_dict = Shop.objects.in_bulk(page_obj.object_list)
    shops_list = [shops_dict[shop_id] for shop_id in page_obj.object_list if shop_id in shops_dict]

    if request.GET.get('ajax') == '1':
        if int(page_number) > paginator.num_pages:
            return HttpResponse('')
        return render(request, 'pages/_shop_cards.html', {'shops': shops_list})

    return render(request, 'pages/home.html', {
        'shops': shops_list,
        'page_obj': page_obj,
        'selected_location': selected_location,
        'location_id': location_id or '',
})


    # shops_dict = Shop.objects.in_bulk(page_obj.object_list)
    # shops = [shops_dict[shop_id] for shop_id in page_obj.object_list if shop_id in shops_dict]

    # return render(request, 'pages/home.html', {
    #     'shops': shops,
    #     'page_obj': page_obj,
    #     'selected_location': selected_location,
    #     'location_id': location_id or '',
    # })


# from django.shortcuts import render
# from shops.models import Shop
# from locations.models import Location


# def get_descendant_ids(location):
#     ids = [location.id]
#     for child in location.children.all():
#         ids.append(child.id)
#         ids += list(child.children.values_list('id', flat=True))
#     return ids


# def home(request):
#     location_id = request.GET.get('location')
#     shops = Shop.objects.filter(is_active=True)

#     selected_location = None
#     if location_id:
#         selected_location = Location.objects.filter(id=location_id).first()
#         if selected_location:
#             ids = get_descendant_ids(selected_location)
#             shops = shops.filter(location_id__in=ids)

#     return render(request, 'pages/home.html', {
#         'shops': shops,
#         'selected_location': selected_location,
#     })