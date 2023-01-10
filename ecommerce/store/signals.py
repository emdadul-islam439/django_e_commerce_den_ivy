from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from store.models import Product, Stock, OrderItem, SoldItem
    
@receiver(post_save, sender = Product)    
def create_new_stock_item(sender, instance, created, **kwargs):
    print(f'IN CREATE-NEW-STOCK-ITEM...... sender = {sender} instance = {instance} kwargs = {kwargs}')
    if created:
        Stock.objects.create(product= instance)
    instance.stock.save()
    
@receiver(pre_save, sender = OrderItem)
def create_sold_item(sender, instance, **kwargs):
    print(f'IN CREATE-SOLD_ITEM...... sender = {sender} instance = {instance} kwargs = {kwargs}')
    
    stockInfo = Stock.objects.get(product=instance.product)
    # solving corner-cases
    if stockInfo.no_of_item_in_stock < instance.quantity:
        raise Exception(f"There is low item quantity of the product {instance.product} in stock.")
    
    SoldItem.objects.create(
        order=instance.order,
        product=instance.product,
        unit_price=stockInfo.current_unit_price,
        purchase_price=stockInfo.current_purchase_price,
        quantity=instance.quantity,
        discount=stockInfo.current_discount
    )