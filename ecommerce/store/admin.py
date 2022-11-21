from django.contrib import admin
from store.models import Customer, Order, OrderItem, Product, Cart, CartItem, ShippingAddress, WishListItem, PurchasedItem, SoldItem, Stock

# Register your models here.
class CustomerAdminModel(admin.ModelAdmin):
    search_fields = ("user__username",)
admin.site.register(Customer, CustomerAdminModel)


class ProductAdminModel(admin.ModelAdmin):
    search_fields=("name",)
admin.site.register(Product, ProductAdminModel)  
      
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(WishListItem)

class PurchasedAdminModel(admin.ModelAdmin):
    list_display=["product", "unit_price", "purchase_price", "quantity", "total_unit_price", "total_purchase_price"]
    list_editable=["unit_price", "purchase_price", "quantity"]
    list_filter=["date_added", "buying_time", "expiry_date", ]
    raw_id_fields=["product",]
    search_fields=["product"]
    autocomplete_fields=["product"]
admin.site.register(PurchasedItem, PurchasedAdminModel)

class SoldAdminModel(admin.ModelAdmin):
    list_display=["product", "customer", "purchase_price", "unit_price", "discount", "unit_selling_price", "quantity", "total_purchase_price", "total_unit_price", "total_discount", "total_selling_price", "total_profit",]
    list_filter=["date_added",]
    raw_id_fields=["product", "customer", ]
    search_fields=("product", "customer")
    autocomplete_fields=("product", "customer")
admin.site.register(SoldItem, SoldAdminModel)

class StockAdminModel(admin.ModelAdmin):
    search_fields=('product__name',)
    list_display= ("product", "current_unit_price", "current_discount", "current_selling_price", "no_of_item_in_stock", "order_limit", "effective_order_limit", "current_purchase_price", "avg_purchase_price", "avg_discount_price", "avg_selling_price",)
    list_editable = ["current_discount", "order_limit",]
    raw_id_fields = ["product",]
admin.site.register(Stock, StockAdminModel)