from django.urls import path, include,re_path
from . import views

urlpatterns = [
    path('carts/', views.carts, name='carts'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),



]
