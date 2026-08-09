


from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem


def checkout(request):
    cart = Cart(request)

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