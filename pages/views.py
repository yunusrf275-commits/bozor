
import random
from django.http import HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from categories.models import Category
from shops.models import Shop
from locations.models import Location


def get_descendant_ids(location):
    ids = [location.id]
    for child in location.children.all():
        ids.append(child.id)
        ids += list(child.children.values_list('id', flat=True))
    return ids


def get_category_descendant_ids(category):
    ids = [category.id]
    for child in category.children.all():
        ids.append(child.id)
        ids += list(child.children.values_list('id', flat=True))
    return ids


from products.models import Product

def home(request):
    location_id = request.GET.get('location')
    category_id = request.GET.get('category')
    query = request.GET.get('q', '').strip()
    view_mode = request.GET.get('view', 'shops')  # 'shops' или 'products'
    page_number = request.GET.get('page', 1)

    if view_mode == 'products':
        products_qs = Product.objects.filter(is_active=True, shop__is_active=True)

        selected_location = None
        if location_id:
            selected_location = Location.objects.filter(id=location_id).first()
            if selected_location:
                ids = get_descendant_ids(selected_location)
                products_qs = products_qs.filter(shop__location_id__in=ids)

        if category_id:
            category = Category.objects.filter(id=category_id).first()
            if category:
                cat_ids = get_category_descendant_ids(category)
                products_qs = products_qs.filter(category_id__in=cat_ids)

        if query:
            products_qs = products_qs.filter(name__icontains=query)

        session_key = f"products_order_{location_id or 'all'}_{category_id or 'all'}_{query or 'none'}"

        if session_key not in request.session:
            ids_list = list(products_qs.values_list('id', flat=True))
            random.shuffle(ids_list)
            request.session[session_key] = ids_list
        else:
            ids_list = request.session[session_key]

        paginator = Paginator(ids_list, 20)
        page_obj = paginator.get_page(page_number)

        products_dict = Product.objects.in_bulk(page_obj.object_list)
        products_list = [products_dict[pid] for pid in page_obj.object_list if pid in products_dict]

        if request.GET.get('ajax') == '1':
            if int(page_number) > paginator.num_pages:
                return HttpResponse('')
            return render(request, 'pages/_product_cards.html', {'products': products_list})

        return render(request, 'pages/home.html', {
            'view_mode': view_mode,
            'products': products_list,
            'page_obj': page_obj,
            'location_id': location_id or '',
            'category_id': category_id or '',
            'query': query,
        })

    # --- дальше идёт весь существующий код для магазинов (shops), без изменений ---
    shops_qs = Shop.objects.filter(is_active=True)
    # ... остальное как было

    shops_qs = Shop.objects.filter(is_active=True)

    selected_location = None
    if location_id:
        selected_location = Location.objects.filter(id=location_id).first()
        if selected_location:
            ids = get_descendant_ids(selected_location)
            shops_qs = shops_qs.filter(location_id__in=ids)

    if category_id:
        category = Category.objects.filter(id=category_id).first()
        if category:
            cat_ids = get_category_descendant_ids(category)
            shops_qs = shops_qs.filter(products__category_id__in=cat_ids).distinct()

    if query:
        shops_qs = shops_qs.filter(products__name__icontains=query, products__is_active=True).distinct()

    # session_key теперь учитывает и запрос
    session_key = f"shops_order_{location_id or 'all'}_{category_id or 'all'}_{query or 'none'}"

    # ... остальной код без изменений, только session_key заменить на этот

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
        'view_mode': view_mode,
        'shops': shops_list,
        'page_obj': page_obj,
        'selected_location': selected_location,
        'location_id': location_id or '',
        'category_id': category_id or '',
        'query': query,
})


    