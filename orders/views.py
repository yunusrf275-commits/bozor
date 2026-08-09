


from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from shops.models import Shop
from .models import Order, OrderItem

from django.contrib.auth.decorators import login_required


def checkout(request):
    cart = Cart(request)
#     order = Order.objects.create(
#     shop=shop,
#     customer=request.user if request.user.is_authenticated else None,
#     customer_phone=phone,
#     customer_name=name,
# )

    if len(cart) == 0:
        return redirect('cart:detail')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        name = request.POST.get('name', '')

        if not phone:
            messages.error(request, 'Укажите номер телефона.')
            return render(request, 'orders/checkout.html', {'cart': cart})

        # Разбиваем корзину по магазинам — один заказ на магазин
        shops_items = {}
        for item in cart:
            shop = item['product'].shop
            shops_items.setdefault(shop, []).append(item)

        created_orders = []
        for shop, items in shops_items.items():
            order = Order.objects.create(
                shop=shop,
                customer_phone=phone,
                customer_name=name,
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price_at_order=item['product'].final_price,
                )
            created_orders.append(order)

        cart.clear()

        return render(request, 'orders/success.html', {'orders': created_orders})

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related('items__product', 'shop')
    return render(request, 'orders/my_orders.html', {'orders': orders})