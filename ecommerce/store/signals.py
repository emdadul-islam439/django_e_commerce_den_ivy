from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Product, Stock
    
@receiver(post_save, sender = Product)    
def create_new_stock_item(sender, instance, created, **kwargs):
    print(f'IN CREATE-NEW-STOCK-ITEM...... sender = {sender} instance = {instance} kwargs = {kwargs}')
    if created:
        Stock.objects.create(product= instance)
    instance.stock.save()