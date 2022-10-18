import json
from django.shortcuts import render
from store.models import Cart, Product, CartItem, ShippingAddress, WishListItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from . utils import cartData, guestOrder, cookieCart, getWishListItems
from django.views.generic import DetailView
from django.contrib import messages

# Create your views here.
def store(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
        
    products = Product.objects.all()
    print(f'........STORE PAGE......  noOfCartItems = {noOfCartItems}')
    context={ 'products' : products, 'noOfCartItems':  noOfCartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
    cart = cookieData['cart']
    items = cookieData['items']
    
    context={ 'items': items, 'cart': cart, 'noOfCartItems':  noOfCartItems }
    if not request.user.is_authenticated:
        messages.success(request, "Guest Checkout Feature!! You can now order without Login into the site! If all the cart-items are digital, you will not have to give your shipping address also!")
    return render(request, 'store/cart.html', context)


def checkout(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
    cart = cookieData['cart']
    items = cookieData['items']
    
    context={ 'items': items, 'cart': cart, 'noOfCartItems':  noOfCartItems }
    if not request.user.is_authenticated:
        messages.success(request, "You can now order from us without Login into the site!")
    return render(request, 'store/checkout.html', context)


# @csrf_exempt
def UpdateItem(request):
    data = json.loads(request.body)
    
    action = data['action']
    productId = data['productId']
    
    print(f"productId = {productId} ")
    print(f"action = {action}")
    
    customer = request.user.customer
    product = Product.objects.get(id = productId)
    cart, created = Cart.objects.get_or_create(customer = customer)
    cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if action == 'add':
        cartItem.quantity += 1
        response_message = 'Item was ADDED successfully'
    elif action == 'remove':
        cartItem.quantity -= 1
        response_message = 'Item was DELETED successfully'
    
    cartItem.save()
    
    if cartItem.quantity <= 0:
        cartItem.delete()
    
    return JsonResponse(response_message, safe=False)



def processOrder(request):
    print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(f"Data : {data}")
    
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer = customer)
    else:
        customer, cart = guestOrder(request= request, data= data)
        
    total = float(data['form']['total'])
    cart.transaction_id = transaction_id
    
    if total == cart.get_cart_total:
        now_time = datetime.datetime.now()
        print(f'now_time = {now_time}  type(now_time) = {type(now_time)}')
        cart.modified = now_time
    cart.save()
    
    if cart.shipping == True:
        ShippingAddress.objects.create( 
            customer = customer,
            cart = cart,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    return JsonResponse('Payment Completed...', safe=False)



def updateWishList(request):
    print('Data: ', request.body)
    
    data = json.loads(request.body)
    print(f"Data : {data}")
    response = ''
    
    if request.user.is_authenticated:
        customer = request.user.customer
        product_id = data['productId']
        product = Product.objects.get(id = product_id)
        print(f'customer = {customer} | product_id = {product_id} | product.name = {product.name} ')
        wishListItem, created = WishListItem.objects.get_or_create(customer = customer, product = product)
        
        if data['action'] == 'add':
            wishListItem.save()
            response = 'Added to wish-list'
        elif data['action'] == 'remove':
            wishListItem.delete()
            response = 'Removed from wish-list'
    else:
        pass
    
    return JsonResponse(response, safe=False)


class ProductDetailView(DetailView):
    template_name: str = "store/product-details.html"
    context_object_name: str = "product"
    model = Product
    
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        context['item'] = self.item
        context['noOfCartItems'] = self.noOfCartItems
        context['isInWishlist'] = self.is_in_wishlist
        return context
    
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request = request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.items = self.cookieData['items']
        self.product_id = self.kwargs.get('pk')
        self.user_wishlist = [] if (request.user.is_anonymous) else WishListItem.objects.filter(product__id = self.product_id, customer = request.user.customer)
        self.is_in_wishlist = len(self.user_wishlist) > 0
        
        found_item = False
        for item in self.items:
            print(f'type(item) = {type(item)}  type(product_id) = {type(self.product_id)}')
            item_product_id = item.product.id if(request.user.is_authenticated) else item['product']['id']
            if item_product_id == self.product_id:
                self.item = item
                found_item = True
                break
        
        if not found_item:
            self.item = "NONE"
        print(f'product_id = {self.product_id}  item = {self.item},  noOfCartItems = {self.noOfCartItems},  user_wishlist = {self.user_wishlist}')
        return super(ProductDetailView, self).get(request, *args, **kwargs)