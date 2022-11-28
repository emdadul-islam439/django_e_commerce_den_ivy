from email.policy import default
from random import choices
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='', related_name='customer', null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    image = models.ImageField(default = 'default.png', upload_to = "profile_pics")
    
    def __str__(self) -> str:
        return str(self.user)
    

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(default=0.0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
  
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        
        return url
    
    
    @property
    def isInWishlist(self):
        wishlist_items = self.wishlistitem_set.all()
        if len(wishlist_items) > 0:
            return "True" 
        else:
            return "False"
    
    
    @property
    def wishlist_item_customer_list(self):
        wishlist_items = self.wishlistitem_set.all()
        print('wishlist_items: ', wishlist_items)
        
        customer_list = []
        for wish_item in wishlist_items:
            print('adding customer.user = ', wish_item.customer)
            customer_list.append(wish_item.customer)
        
        print('returning...  user_list = ', customer_list)
        return customer_list
    
    
    @property
    def get_current_unit_price(self):
        stock_info = self.stock_set.all().first()
        return stock_info.current_unit_price
    
    @property
    def get_current_discount(self):
        stock_info = self.stock_set.all().first()
        return stock_info.current_discount
    
    @property
    def get_current_selling_price(self):
        stock_info = self.stock_set.all().first()
        return stock_info.get_current_selling_price
    
    @property
    def get_stock_info(self):
        stock_info = self.stock_set.all().first()
        return stock_info
    
    
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self) -> str:
        return f'Cart ID: {self.id}    -   Customer: {self.customer.user}'
    
    @property
    def shipping(self):
        shipping = False
        cart_items = self.cartitem_set.all()
        
        for item in cart_items:
            if item.product.digital == False:
                shipping = True
                break
        return shipping
    
    @property
    def get_cart_total(self):
        cart_items = self.cartitem_set.filter(is_checked = True)
        total = sum([item.get_total for item in cart_items])
        return total 
    
    @property
    def get_all_cart_item_count(self):
        cart_items = self.cartitem_set.all()
        total = sum([item.quantity for item in cart_items])
        return total 
    
    @property
    def get_checked_item_count(self):
        cart_items = self.cartitem_set.filter(is_checked = True)
        total = sum([item.quantity for item in cart_items])
        return total 
    
    
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    is_checked = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'CartItem ID: {self.id}  ->   Name: {self.product.name}'
    
    @property
    def get_total(self):
        return self.quantity * self.product.price
    
    @property
    def get_stock_info(self):
        stock_item = Stock.objects.all().first()
        return stock_item
    


class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'Waiting for Payment'),
        (1, 'Preparing Order'),
        (2, 'Order is Prepared'),
        (3, 'Order in Shipping'),
        (4, 'Order is Delivered'),
        (5, 'Cancelled')
    )
    
    PAYMENT_OPTION_CHOICES = (
        ('Cash On Delivery', 'Cash On Delivery'),
        ('Bkash', 'Bkash'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.IntegerField('Order Status', choices=STATUS_CHOICES, default=0)
    payment_option = models.CharField('Payment Options', choices=PAYMENT_OPTION_CHOICES, max_length=20, default='Cash On Delivery')
    created = models.DateTimeField('Created in', auto_now_add=True)
    modified = models.DateTimeField('Modified in', auto_now=True)
    transaction_id = models.CharField(max_length=100, null=True)
    
    class Meta:
        verbose_name = 'Order'
        ordering = ('-created',)
    
    def __str__(self) -> str:
        return f'Order #{self.pk}     -     Customer: {self.customer.user}'
    
    @property
    def products(self):
        products_ids = self.items.values_list('product')
        return Product.objects.filter(pk__in=products_ids)
    
    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()
        
        for item in order_items:
            if item.product.digital == False:
                shipping = True
                break
        return shipping
    
    @property
    def get_order_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total 
    
    @property
    def get_number_of_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total 

        
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'OrderItem ID: {self.id}  ->   Name: {self.product.name}'
    
    @property
    def get_total(self):
        return self.quantity * self.product.price
        
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True) 
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.address
    
    
    
class WishListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'WishListItem: product-name = {self.product.name} | customer = {self.customer}'
    
    
    
class PurchasedItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.FloatField()
    purchase_price = models.FloatField()
    quantity = models.IntegerField(default = 0)
    product_source_name = models.CharField(max_length=200, null=True)
    buying_time = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'PurchasedItem: product-name = {self.product.name} | unit_price = {self.unit_price}  |  quantity = {self.quantity}'
    
    @property
    def total_unit_price(self):
        return self.unit_price * self.quantity
    
    @property
    def total_purchase_price(self):
        return self.purchase_price * self.quantity
    
    
        
class SoldItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.FloatField(default=0.0)
    purchase_price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default = 0)
    discount = models.FloatField(default=0.0)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'SellingItem: product-name = {self.product.name} | customer = {self.customer}'
    
    @property
    def unit_selling_price(self):
        return self.unit_price - self.discount
    
    @property
    def total_unit_price(self):
        return self.unit_price * self.quantity
    
    @property
    def total_purchase_price(self):
        return self.purchase_price * self.quantity
    
    @property
    def total_discount(self):
        return self.discount * self.quantity
    
    @property
    def total_selling_price(self):
        return self.unit_selling_price * self.quantity
    
    @property
    def unit_profit(self):
        return self.unit_selling_price - self.purchase_price
    
    @property
    def total_profit(self):
        return self.unit_profit * self.quantity
    
    

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    current_discount = models.FloatField()
    order_limit = models.IntegerField(default=50)
    
    
    def __str__(self) -> str:
        return f'Stock: product-name = {self.product.name}'
    
    @property
    def current_unit_price(self):
        all_purchased_items = PurchasedItem.objects.filter(product=self.product)
        total_purchase_count = len(all_purchased_items)
        return 0 if total_purchase_count == 0 else all_purchased_items[total_purchase_count - 1].unit_price
        
    
    @property
    def current_selling_price(self):
        return self.current_unit_price - self.current_discount
    
    @property
    def current_purchase_price(self):
        all_purchased_items = PurchasedItem.objects.filter(product=self.product)
        total_purchase_count = len(all_purchased_items)
        return 0 if total_purchase_count == 0 else all_purchased_items[total_purchase_count - 1].purchase_price
    
    @property 
    def avg_purchase_price(self):
        all_purchased_items = PurchasedItem.objects.filter(product=self.product)
        total_purchase_count = len(all_purchased_items)
        
        sum_of_purchase_price = sum([item.purchase_price for item in all_purchased_items]) if total_purchase_count > 0 else 0
        return 0 if total_purchase_count == 0 else sum_of_purchase_price / total_purchase_count
    
    @property
    def avg_discount_price(self):
        all_sold_items = SoldItem.objects.filter(product=self.product)
        total_sell_count = len(all_sold_items)
        
        sum_of_discount_price = sum([item.discount for item in all_sold_items]) if total_sell_count > 0 else 0
        return  0 if total_sell_count == 0 else sum_of_discount_price / total_sell_count
    
    @property
    def avg_selling_price(self):
        all_sold_items = SoldItem.objects.filter(product=self.product)
        total_sell_count = len(all_sold_items)
        
        sum_of_selling_price = sum([item.discount for item in all_sold_items]) if total_sell_count > 0 else 0
        return  0 if total_sell_count == 0 else sum_of_selling_price / total_sell_count
        
        
    @property
    def no_of_purchased_unit(self):
        all_purchased_items = PurchasedItem.objects.filter(product=self.product)
        sum_of_purchase_quantity = sum([item.quantity for item in all_purchased_items]) if len(all_purchased_items) > 0 else 0
        return sum_of_purchase_quantity
        
    
    @property 
    def no_of_sold_unit(self):
        all_sold_items = SoldItem.objects.filter(product=self.product)
        sum_of_sold_unit = sum([item.quantity for item in all_sold_items]) if len(all_sold_items) > 0 else 0
        return sum_of_sold_unit
    
    
    @property
    def no_of_item_in_stock(self):
        return self.no_of_purchased_unit - self.no_of_sold_unit
    
    
    @property
    def effective_order_limit(self):
        return min(self.order_limit, self.no_of_item_in_stock)
    