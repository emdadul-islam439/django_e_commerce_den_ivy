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
    order_limit = models.IntegerField(default=50)
    
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
    def get_product_price(self):
        return self.price
    
    
    
    
class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self) -> str:
        return f'Cart ID: {self.id}'
    
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
        return f'Order #{self.pk}'
    
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