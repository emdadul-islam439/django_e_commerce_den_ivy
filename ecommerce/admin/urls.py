from . import views as admin_views
from django.urls import path
from django.contrib import admin
urlpatterns = [
    path('store/order/<int:pk>/change/update-admin-order-status/', admin_views.updateAdminOrderStatus, name="update-admin-order-status"),
    path('store/order/<int:pk>/change/update-admin-order-item/', admin_views.updateAdminOrderItem, name="update-admin-order-item"),
    path('store/order/<int:pk>/change/remove-admin-order-item/', admin_views.removeAdminOrderItem, name="remove-admin-order-item"),
    path('store/order/<int:pk>/change/add-admin-order-items/', admin_views.addAdminOrderItems, name="add-admin-order-items"),
    path('store/order/<int:pk>/change/', admin_views.AdminOrderDetailView.as_view(), name="admin-order-details"),
    path('', admin.site.urls),
]
