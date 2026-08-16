

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('my/', views.my_orders, name='my_orders'),
    path('success/', views.order_success, name='success'),
    path('<int:order_id>/qr/', views.order_qr_code, name='order_qr'),
]