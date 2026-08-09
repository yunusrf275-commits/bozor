from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from shops.models import Shop
from .models import User





def seller_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == User.ROLE_SHOP_OWNER and not user.is_staff:
            login(request, user)
            return redirect('accounts:seller_dashboard')
        else:
            messages.error(request, 'Неверный логин, пароль или у вас нет доступа продавца.')

    return render(request, 'accounts/seller_login.html')


@login_required
def seller_dashboard(request):
    if request.user.role != User.ROLE_SHOP_OWNER:
        return redirect('accounts:seller_login')

    owned_shops = Shop.objects.filter(owner=request.user)
    staff_shops = Shop.objects.filter(staff__user=request.user)
    my_shops = (owned_shops | staff_shops).distinct()

    if my_shops.count() == 1:
        return redirect('shops:dashboard', shop_id=my_shops.first().id)

    return render(request, 'accounts/seller_dashboard.html', {'shops': my_shops})



def customer_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return render(request, 'accounts/customer_register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким логином уже существует.')
            return render(request, 'accounts/customer_register.html')

        user = User.objects.create_user(
            username=username,
            phone=phone,
            password=password,
            role=User.ROLE_CUSTOMER,
        )
        login(request, user)
        return redirect('pages:home')

    return render(request, 'accounts/customer_register.html')


def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == User.ROLE_CUSTOMER and not user.is_staff:
            login(request, user)
            return redirect('pages:home')
        else:
            messages.error(request, 'Неверный логин или пароль.')

    return render(request, 'accounts/customer_login.html')


def customer_logout(request):
    logout(request)
    return redirect('pages:home')
