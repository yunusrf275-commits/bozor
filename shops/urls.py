

from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('<int:shop_id>/dashboard/', views.shop_dashboard, name='dashboard'),
    path('<int:shop_id>/products/add/', views.product_add, name='product_add'),
    path('<int:shop_id>/products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('<int:shop_id>/products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('<slug:slug>/', views.shop_detail, name='detail'),
    path('<int:shop_id>/orders/<int:order_id>/status/', views.order_update_status, name='order_update_status'),
    path('<int:shop_id>/staff/', views.staff_list, name='staff_list'),
    path('<int:shop_id>/staff/add/', views.staff_add, name='staff_add'),
    path('<int:shop_id>/staff/<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),
    path('<int:shop_id>/settings/', views.shop_settings, name='settings'),
    path('<int:shop_id>/products/', views.shop_products, name='products'),
    path('<int:shop_id>/orders/', views.shop_orders, name='orders'),

]