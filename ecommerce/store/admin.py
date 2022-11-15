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

class StockAdminModel(admin.ModelAdmin):
    search_fields=('product__name',)
    list_display= ("product", "current_unit_price", "current_discount", "current_selling_price", "no_of_item_in_stock", "avg_purchase_price", "avg_discount_price", "avg_selling_price",)
    list_editable = ["current_unit_price", "current_discount",]
admin.site.register(Stock, StockAdminModel)