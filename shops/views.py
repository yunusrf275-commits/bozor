

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Shop


@login_required
def shop_dashboard(request, shop_id):
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)
    return render(request, 'shops/dashboard.html', {'shop': shop})
