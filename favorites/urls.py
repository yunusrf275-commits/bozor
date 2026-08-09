

from django.urls import path
from . import views

app_name = 'favorites'

urlpatterns = [
    path('shop/<int:shop_id>/toggle/', views.toggle_favorite_shop, name='toggle_shop'),
    path('product/<int:product_id>/toggle/', views.toggle_favorite_product, name='toggle_product'),
    path('my/', views.my_favorites, name='my_favorites'),
]