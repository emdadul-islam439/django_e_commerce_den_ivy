from django.urls import path
from django.contrib import admin

from . import views as admin_views

urlpatterns = [
    path('store/order/<int:pk>/change/update-admin-order-status/', admin_views.updateAdminOrderStatus, name="update-admin-order-status"),
    path('store/order/<int:pk>/change/update-admin-order-item/', admin_views.updateAdminOrderItem, name="update-admin-order-item"),
    path('store/order/<int:pk>/change/remove-admin-order-item/', admin_views.removeAdminOrderItem, name="remove-admin-order-item"),
    path('store/order/<int:pk>/change/add-admin-order-items/', admin_views.addAdminOrderItems, name="add-admin-order-items"),
    path('store/order/<int:pk>/change/', admin_views.AdminOrderDetailView.as_view(), name="admin-order-details"),
    
    path('store/cart/<int:pk>/change/update-admin-cart-item/', admin_views.updateAdminCartItem, name="update-admin-cart-item"),
    path('store/cart/<int:pk>/change/remove-admin-cart-item/', admin_views.removeAdminCartItem, name="remove-admin-cart-item"),
    path('store/cart/<int:pk>/change/add-admin-cart-items/', admin_views.addAdminCartItems, name="add-admin-cart-items"),
    path('store/cart/<int:pk>/change/', admin_views.AdminCartDetailView.as_view(), name="admin-cart-details"),
    
    path('', admin.site.urls),
]
