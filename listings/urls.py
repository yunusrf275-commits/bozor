

from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('create/', views.create_listing, name='create'),
    path('', views.listing_list, name='list'),
    path('my/', views.my_listings, name='my_listings'),
]