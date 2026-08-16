


from django.shortcuts import render, redirect
from django.contrib import messages
from cart.cart import Cart
from shops.models import Shop
from .models import Order, OrderItem

from django.contrib.auth.decorators import login_required

from notifications.models import Notification

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

        shops_items = {}
        for item in cart:
            shop = item['product'].shop
            shops_items.setdefault(shop, []).append(item)

        created_order_ids = []
        for shop, items in shops_items.items():
            order = Order.objects.create(
                shop=shop,
                customer=request.user if request.user.is_authenticated else None,
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

            recipients = [shop.owner] if shop.owner else []
            recipients += [staff.user for staff in shop.staff.all()]
            for recipient in set(recipients):
                Notification.objects.create(
                    user=recipient,
                    text=f"Новый заказ #{order.id} на сумму {order.total_price} сум",
                    link=f"/shops/{shop.id}/dashboard/",
                )

            created_order_ids.append(order.id)

        cart.clear()
        request.session['last_order_ids'] = created_order_ids

        return redirect('orders:success')

    return render(request, 'orders/checkout.html', {'cart': cart})


def order_success(request):
    order_ids = request.session.get('last_order_ids', [])
    orders = Order.objects.filter(id__in=order_ids)
    return render(request, 'orders/success.html', {'orders': orders})

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related('items__product', 'shop')
    return render(request, 'orders/my_orders.html', {'orders': orders})