

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from shops.models import Shop
from products.models import Product
from orders.models import OrderItem
from .models import ShopReview, ProductReview


@login_required
def add_shop_review(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)

    has_purchased = OrderItem.objects.filter(
        order__shop=shop,
        order__customer=request.user,
    ).exists()

    if not has_purchased:
        messages.error(request, 'Оставить отзыв можно только после покупки в этом магазине.')
        return redirect('shops:detail', slug=shop.slug)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text', '')

        ShopReview.objects.update_or_create(
            shop=shop,
            user=request.user,
            defaults={'rating': rating, 'text': text},
        )
        messages.success(request, 'Спасибо за отзыв!')

    return redirect('shops:detail', slug=shop.slug)


@login_required
def add_product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    has_purchased = OrderItem.objects.filter(
        order__customer=request.user,
        product=product,
    ).exists()

    if not has_purchased:
        messages.error(request, 'Оставить отзыв можно только после покупки этого товара.')
        return redirect('products:detail', slug=product.slug)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        text = request.POST.get('text', '')

        ProductReview.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={'rating': rating, 'text': text},
        )
        messages.success(request, 'Спасибо за отзыв!')

    return redirect('products:detail', slug=product.slug)
