

from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('<int:shop_id>/dashboard/', views.shop_dashboard, name='dashboard'),
]