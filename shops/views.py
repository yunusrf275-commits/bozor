


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shop
from products.models import Product, ProductImage
from categories.models import Category
from .models import Shop, ShopStaff
from orders.models import Order

from django.contrib.auth import get_user_model
from django.contrib import messages

from notifications.models import Notification


def shop_detail(request, slug):
    shop = get_object_or_404(Shop, slug=slug, is_active=True)
    products = Product.objects.filter(shop=shop, is_active=True)
    reviews = shop.reviews.select_related('user')

    favorite_shop_ids = []
    can_review = False
    if request.user.is_authenticated:
        favorite_shop_ids = list(request.user.favorite_shops.values_list('shop_id', flat=True))
        from orders.models import OrderItem
        can_review = OrderItem.objects.filter(order__shop=shop, order__customer=request.user).exists()

    return render(request, 'shops/detail.html', {
        'shop': shop,
        'products': products,
        'favorite_shop_ids': favorite_shop_ids,
        'reviews': reviews,
        'can_review': can_review,
    })



@login_required
def shop_dashboard(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    access_role = get_shop_access(request.user, shop)

    if access_role is None:
        return redirect('accounts:seller_login')

    products = Product.objects.filter(shop=shop)
    orders = Order.objects.filter(shop=shop).prefetch_related('items__product')

    can_manage_products = access_role in ('owner', ShopStaff.ROLE_MANAGER, ShopStaff.ROLE_PRODUCT_MANAGER)
    can_manage_orders = access_role in ('owner', ShopStaff.ROLE_MANAGER, ShopStaff.ROLE_ORDER_HANDLER)

    return render(request, 'shops/dashboard.html', {
        'shop': shop,
        'products': products,
        'orders': orders,
        'access_role': access_role,
        'can_manage_products': can_manage_products,
        'can_manage_orders': can_manage_orders,
    })


@login_required
def product_add(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id)
    access_role = get_shop_access(request.user, shop)

    if access_role not in ('owner', ShopStaff.ROLE_MANAGER, ShopStaff.ROLE_PRODUCT_MANAGER):
        return redirect('shops:dashboard', shop_id=shop.id)

    # ... остальной код без изменений (только shop уже переопределён выше)
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
    shop = get_object_or_404(Shop, id=shop_id)
    access_role = get_shop_access(request.user, shop)

    if access_role not in ('owner', ShopStaff.ROLE_MANAGER, ShopStaff.ROLE_PRODUCT_MANAGER):
        return redirect('shops:dashboard', shop_id=shop.id)
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
    shop = get_object_or_404(Shop, id=shop_id)
    access_role = get_shop_access(request.user, shop)

    if access_role not in ('owner', ShopStaff.ROLE_MANAGER, ShopStaff.ROLE_PRODUCT_MANAGER):
        return redirect('shops:dashboard', shop_id=shop.id)
    product = get_object_or_404(Product, id=product_id, shop=shop)

    if request.method == 'POST':
        product.delete()
        return redirect('shops:dashboard', shop_id=shop.id)

    return render(request, 'shops/product_confirm_delete.html', {'shop': shop, 'product': product})



@login_required
def order_update_status(request, shop_id, order_id):
    shop = get_object_or_404(Shop, id=shop_id)
    access_role = get_shop_access(request.user, shop)

    if access_role not in ('owner', ShopStaff.ROLE_MANAGER, ShopStaff.ROLE_ORDER_HANDLER):
        return redirect('shops:dashboard', shop_id=shop.id)

    order = get_object_or_404(Order, id=order_id, shop=shop)
    # ... остальной код без изменений
    order = get_object_or_404(Order, id=order_id, shop=shop)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if new_status in valid_statuses:
            order.status = new_status
            order.save()

            if order.customer:
                Notification.objects.create(
                    user=order.customer,
                    text=f"Статус вашего заказа #{order.id} изменён: {order.get_status_display()}",
                    link=f"/orders/my/",
                )

    return redirect('shops:dashboard', shop_id=shop.id)



def get_shop_access(user, shop):
    """
    Возвращает роль пользователя в магазине, или None, если доступа нет.
    Владелец магазина всегда имеет полный доступ (роль 'owner').
    """
    if shop.owner_id == user.id:
        return 'owner'

    staff = ShopStaff.objects.filter(shop=shop, user=user).first()
    if staff:
        return staff.role

    return None



User = get_user_model()


@login_required
def staff_list(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)  # только владелец
    staff_members = ShopStaff.objects.filter(shop=shop).select_related('user')
    return render(request, 'shops/staff_list.html', {'shop': shop, 'staff_members': staff_members})


@login_required
def staff_add(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)  # только владелец

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name', '')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'shops/staff_form.html', {'shop': shop, 'roles': ShopStaff.ROLE_CHOICES})

        new_user = User.objects.create_user(
            username=username,
            first_name=first_name,
            password=password,
            role=User.ROLE_SHOP_OWNER,  # техническая роль в системе входа — та же, что у владельца, чтобы сотрудник заходил через тот же вход продавца
        )

        ShopStaff.objects.create(shop=shop, user=new_user, role=role)

        messages.success(request, f'Сотрудник {username} добавлен.')
        return redirect('shops:staff_list', shop_id=shop.id)

    return render(request, 'shops/staff_form.html', {'shop': shop, 'roles': ShopStaff.ROLE_CHOICES})


@login_required
def staff_delete(request, shop_id, staff_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)  # только владелец
    staff = get_object_or_404(ShopStaff, id=staff_id, shop=shop)

    if request.method == 'POST':
        staff.delete()  # удаляет только связь сотрудник-магазин, не сам аккаунт User
        messages.success(request, 'Сотрудник удалён из магазина.')

    return redirect('shops:staff_list', shop_id=shop.id)
