

from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)

    is_favorite_product = False
    if request.user.is_authenticated:
        is_favorite_product = product.favorited_by.filter(user=request.user).exists()

    return render(request, 'products/detail.html', {
        'product': product,
        'is_favorite_product': is_favorite_product,
    })