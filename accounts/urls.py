

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('seller/login/', views.seller_login, name='seller_login'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('register/', views.customer_register, name='customer_register'),
    path('login/', views.customer_login, name='customer_login'),
    path('logout/', views.customer_logout, name='customer_logout'),
    path('seller/', views.seller_landing, name='seller_landing'),
]