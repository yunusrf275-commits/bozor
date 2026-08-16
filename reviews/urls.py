

from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('shop/<int:shop_id>/add/', views.add_shop_review, name='add_shop_review'),
    path('product/<int:product_id>/add/', views.add_product_review, name='add_product_review'),
]