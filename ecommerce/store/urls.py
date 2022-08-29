from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update_item/', views.UpdateItem, name = 'update_item'),
]