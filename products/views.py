

from django.shortcuts import render, get_object_or_404
from .models import Product


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.select_related('user')

    is_favorite_product = False
    can_review = False
    if request.user.is_authenticated:
        is_favorite_product = product.favorited_by.filter(user=request.user).exists()
        from orders.models import OrderItem
        can_review = OrderItem.objects.filter(order__customer=request.user, product=product).exists()

    return render(request, 'products/detail.html', {
        'product': product,
        'is_favorite_product': is_favorite_product,
        'reviews': reviews,
        'can_review': can_review,
    })