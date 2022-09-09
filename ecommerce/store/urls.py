from django.contrib import admin
from django.urls import path
from store import views
from store.views import ProductDetailView

urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart/', views.cart, name = 'cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('update_item/', views.UpdateItem, name = 'update_item'),
    path('process_order/', views.processOrder, name = 'process_order'),
    path('update_wish_list/', views.updateWishList, name = 'update_wish_list'),
    path('product-details/<int:pk>', ProductDetailView.as_view(), name = 'producut-details'),
]