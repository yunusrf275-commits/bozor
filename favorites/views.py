

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from shops.models import Shop
from products.models import Product
from .models import FavoriteShop, FavoriteProduct


@login_required
def toggle_favorite_shop(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    favorite, created = FavoriteShop.objects.get_or_create(user=request.user, shop=shop)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})

    return redirect('shops:detail', slug=shop.slug)


@login_required
def toggle_favorite_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = FavoriteProduct.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite})

    return redirect('products:detail', slug=product.slug)

@login_required
def my_favorites(request):
    favorite_shops = Shop.objects.filter(favorited_by__user=request.user)
    favorite_products = Product.objects.filter(favorited_by__user=request.user)
    return render(request, 'favorites/my_favorites.html', {
        'favorite_shops': favorite_shops,
        'favorite_products': favorite_products,
    })