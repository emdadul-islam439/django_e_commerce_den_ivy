from django.contrib import admin
from store.models import Customer, Product, Cart, CartItem, ShippingAddress, WishListItem

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)        
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(ShippingAddress)
admin.site.register(WishListItem)