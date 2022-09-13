from django.contrib import admin
from django.urls import path
from store import views as store_views
from customers import views as customer_views
from store.views import ProductDetailView

urlpatterns = [
    path('', customer_views.redirectUser, name = 'redirect'),
    path('store/', store_views.store, name = 'store'),
    path('cart/', store_views.cart, name = 'cart'),
    path('checkout/', store_views.checkout, name = 'checkout'),
    path('update_item/', store_views.UpdateItem, name = 'update_item'),
    path('process_order/', store_views.processOrder, name = 'process_order'),
    path('update_wish_list/', store_views.updateWishList, name = 'update_wish_list'),
    path('product-details/<int:pk>', ProductDetailView.as_view(), name = 'producut-details'),
]