from django.contrib import admin
from django.urls import path

from store import views as store_views
from customers import views as customer_views

urlpatterns = [
    path('', customer_views.redirectUser, name = 'redirect'),
    path('stock-item-list/', store_views.stockItemList, name='stock-item-list'),
    path('purchased-item-list/', store_views.purchasedItemList, name='purchased-items-list'),
    path('sold-item-list/', store_views.soldItemList, name='sold-items-list'),
    path('store/', store_views.store, name = 'store'),
    path('cart/', store_views.cart, name = 'cart'),
    path('checkout/', store_views.checkout, name = 'checkout'),
    path('update-registered-user-cart/', store_views.updateRegisteredUserCart, name = 'update-registered-user-cart'),
    path('update-cookie-cart/', store_views.updateCookieCart, name = 'update-cookie-cart'),
    path('update-item/', store_views.updateItem, name = 'update-item'),
    path('process-order/', store_views.processOrder, name = 'process-order'),
    path('complete-payment/', store_views.completePayment, name = 'complete-payment'),
    path('update-wishlist/', store_views.updateWishList, name = 'update-wishlist'),
    path('product-details/<int:pk>', store_views.ProductDetailView.as_view(), name = 'producut-details'),
]   