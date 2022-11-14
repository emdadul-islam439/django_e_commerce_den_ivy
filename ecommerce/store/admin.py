from django.contrib import admin
from store.models import Customer, Order, OrderItem, Product, Cart, CartItem, ShippingAddress, WishListItem, PurchasedItem, SoldItem, Stock

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)        
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(WishListItem)
admin.site.register(PurchasedItem)
admin.site.register(SoldItem)
admin.site.register(Stock)