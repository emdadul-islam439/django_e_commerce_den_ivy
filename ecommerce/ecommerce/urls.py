"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

from customers import views as customer_views

urlpatterns = [
    path('admin/', include("admin.urls")),
    path('register/', customer_views.register, name = "register"),
    path('profile/', customer_views.profile, name = "profile"),
    path('wishlist/', customer_views.wishList, name = 'wishlist'),
    path('order-list/', customer_views.orderList, name = 'order-list'),
    path('order-details/<int:pk>', customer_views.OrderDetailView.as_view(), name = 'order-details'),
    path('login/', auth_views.LoginView.as_view(template_name = "customers/login.html"), name = "login"),
    path('logout/', auth_views.LogoutView.as_view(template_name = "customers/logout.html"), name = "logout"),
    path("", include("store.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)