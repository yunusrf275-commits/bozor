

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shop
from products.models import Product, ProductImage
from categories.models import Category


@login_required
def shop_dashboard(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    products = Product.objects.filter(shop=shop)
    return render(request, 'shops/dashboard.html', {'shop': shop, 'products': products})


@login_required
def product_add(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        discount_percent = request.POST.get('discount_percent') or 0
        stock_quantity = request.POST.get('stock_quantity') or 0
        description = request.POST.get('description', '')

        product = Product.objects.create(
            shop=shop,
            category_id=category_id,
            name=name,
            price=price,
            discount_percent=discount_percent,
            stock_quantity=stock_quantity,
            description=description,
        )

        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)

        return redirect('shops:dashboard', shop_id=shop.id)

    return render(request, 'shops/product_form.html', {'shop': shop, 'categories': categories})


@login_required
def product_edit(request, shop_id, product_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, shop=shop)
    categories = Category.objects.all()

    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.category_id = request.POST.get('category')
        product.price = request.POST.get('price')
        product.discount_percent = request.POST.get('discount_percent') or 0
        product.stock_quantity = request.POST.get('stock_quantity') or 0
        product.description = request.POST.get('description', '')
        product.save()

        for image in request.FILES.getlist('images'):
            ProductImage.objects.create(product=product, image=image)

        return redirect('shops:dashboard', shop_id=shop.id)

    return render(request, 'shops/product_form.html', {'shop': shop, 'categories': categories, 'product': product})


@login_required
def product_delete(request, shop_id, product_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, shop=shop)

    if request.method == 'POST':
        product.delete()
        return redirect('shops:dashboard', shop_id=shop.id)

    return render(request, 'shops/product_confirm_delete.html', {'shop': shop, 'product': product})
