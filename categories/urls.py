

from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    path('get-children/', views.get_children, name='get_children'),
]