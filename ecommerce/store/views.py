from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.contrib import messages

import datetime
import json
from statistics import quantiles

from . utils import cartData, guestOrder, cookieCart, getWishListItems, getCartItemList, getStockInfoList, getProductListFromCartItems
from store.models import Cart, Product, CartItem, ShippingAddress, WishListItem, Order, OrderItem, Stock, PurchasedItem, SoldItem
from background_tasks.models import EmailSendingTask
from background_tasks.enums import SetupStatus
from background_tasks import signals


# Create your views here.
def store(request):
    cookieData = cartData(request=request)
    products = Product.objects.all()
    cartItemList = getCartItemList(request, products, cookieData)
    stockInfoList = getStockInfoList(products)
    
    productInfoList = list(zip(products, cartItemList, stockInfoList))
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}  productInfoList={productInfoList}")
    context={'productInfoList' : productInfoList, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, 'store/store.html', context)


def cart(request):
    cookieData = cartData(request=request)
    items = cookieData['items']
    
    products = getProductListFromCartItems(request, items)
    stockInfoList = getStockInfoList(products)
    
    cartInfoList = list(zip(items, stockInfoList))
    context={'cartInfoList': cartInfoList, 'cart': cookieData['cart'], 'noOfCartItems':  cookieData['noOfCartItems']}
    
    if not request.user.is_authenticated:
        messages.success(request, "Guest Checkout Feature!! You can now order without Login into the site! If all the cart-items are digital, you will not have to give your shipping address also!")
    return render(request, 'store/cart.html', context)


def checkout(request):
    cookieData = cartData(request=request)
    items = cookieData['items']
    checked_item_count = 0
    is_all_item_available = True
    
    for item in items:
        if request.user.is_authenticated:
            if item.is_checked: checked_item_count += 1
            
            stockInfo = Stock.objects.filter(product=item.product).first()
            if stockInfo.effective_order_limit < item.quantity: 
                is_all_item_available = False
        else:
            if item['is_checked']: checked_item_count += 1
            
            product = Product.objects.get(id=item['product']['id'])
            stockInfo = Stock.objects.filter(product=product).first()
            if stockInfo.effective_order_limit < item['quantity']: 
                is_all_item_available = False
        
    if checked_item_count == 0 or not is_all_item_available:
        return redirect('/cart/')
    
    context={ 'items': items, 'cart': cookieData['cart'], 'noOfCartItems':  cookieData['noOfCartItems'] }
    if not request.user.is_authenticated:
        messages.success(request, "You can now order from us without Login into the site!")
    return render(request, 'store/checkout.html', context)


def updateRegisteredUserCart(request):
    print(f"updateRegisteredUserCart---> request.body={request.body}")
    data = json.loads(request.body)
    print(f"cartId = {data['cartId']} ")
    
    cart, created = Cart.objects.get_or_create(id=data['cartId'])
    cartItems = CartItem.objects.filter(cart=cart)
    
    for item in cartItems:
        stockInfo = Stock.objects.filter(product=item.product).first()
        if stockInfo.effective_order_limit == 0:
            item.is_checked = False
        else:
            item.quantity = min(stockInfo.effective_order_limit, item.quantity)
        item.save(update_fields=['is_checked', 'quantity'])
    return JsonResponse('OK', safe=False)


def updateCookieCart(request):
    print(f"updateCookieCart---> request.body={request.body}")
    data = json.loads(request.body)
    cartItems = data['cart']
    print(f"cartItems = {cartItems}")
    
    for itemIdStr in cartItems:
        print(f"itemIdStr = {itemIdStr}......  value = {cartItems[itemIdStr]}")
        product = Product.objects.get(id=itemIdStr)
        stockInfo = Stock.objects.filter(product=product).first()
        if stockInfo.effective_order_limit == 0:
            cartItems[itemIdStr]['is_checked'] = False
        else:
            cartItems[itemIdStr]['quantity'] = min(stockInfo.effective_order_limit, cartItems[itemIdStr]['quantity'])
    
    data['cart'] = cartItems
    return JsonResponse(data, safe=False)


# @csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    
    action = data['action']
    print(f"in UpdateItem()--->    action = {action}")
    
    product = Product.objects.get(id=data['productId'])
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if action == 'add':
        cartItem.quantity += 1
        response_message = 'Item was ADDED successfully'
    elif action == 'remove':
        cartItem.quantity -= 1
        response_message = 'Item was DELETED successfully'
    elif action == 'check-uncheck':
        cartItem.is_checked = not cartItem.is_checked
        response_message = 'Item was CHECKED/UNCHECKED successfully'
    
    cartItem.save(update_fields=['quantity', 'is_checked'])
    if cartItem.quantity <= 0:
        cartItem.delete()
    
    return JsonResponse(response_message, safe=False)


def processOrder(request):
    print('request.body: ', request.body)
    data = json.loads(request.body)
    print(f"data : {data}")
    
    transaction_id = datetime.datetime.now().timestamp()
    
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
    else:
        customer, cart = guestOrder(request=request, data=data)
        
    total = float(data['form']['total'])
    
    if total == cart.get_cart_total:
        now_time = datetime.datetime.now()
        print(f'now_time = {now_time}  type(now_time) = {type(now_time)}')
        
        order = Order.objects.create(
            customer=customer,
            transaction_id=transaction_id
        )
        EmailSendingTask.objects.create(
            order=order,
        )
        
        cartItems = CartItem.objects.filter(cart=cart, is_checked=True)
        for item in cartItems:
            OrderItem.objects.create(
                product=item.product,
                order=order,
                quantity=item.quantity,
            )
            item.delete()
    
    if cart.shipping == True:
        ShippingAddress.objects.create( 
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse(f'{order.id}', safe=False)


def completePayment(request):
    print(f'in completePayment():  data = {request.body}')
    data = json.loads(request.body)
    print(f'data after json-decode = {data}')
    
    order, created = Order.objects.get_or_create(id=data['order_id'])
    
    if order.order_status == 5:
        return_message = 'Order is already cancelled!'
    else:
        order.order_status = 1
        order.save(update_fields=['order_status'])
        
        emailSendingTask = EmailSendingTask.objects.get(order=order)
        emailSendingTask.status = SetupStatus.disabled
        emailSendingTask.save(update_fields=['status'])
        
        return_message = 'success!'
        
    return JsonResponse(return_message, safe=False) 
    

def updateWishList(request):
    print('in updateWishList() --->  Data: ', request.body)
    data = json.loads(request.body)
    print(f"Data : {data}")
    response = ''
    
    if request.user.is_authenticated:
        customer = request.user.customer
        product = Product.objects.get(id=data['productId'])
        print(f"customer = {customer} | product_id = {data['productId']} | product.name = {product.name} ")
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
    template_name: str = "store/product_details.html"
    context_object_name: str = "product"
    model = Product
    
    def get_context_data(self,*args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args,**kwargs)
        context['item'] = self.item
        context['noOfCartItems'] = self.noOfCartItems
        context['isInWishlist'] = self.is_in_wishlist
        return context
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request=request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.items = self.cookieData['items']
        self.product_id = self.kwargs.get('pk')
        self.user_wishlist = [] if (request.user.is_anonymous) else WishListItem.objects.filter(product__id=self.product_id, customer=request.user.customer)
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
    
    
def stockItemList(request):
    cookieData = cartData(request=request)
    products = Stock.objects.all()
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}")
    
    context={ 'stockItemList' : products, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, "admin/store/stock/admin_stock_item_list.html", context)


def purchasedItemList(request):
    cookieData = cartData(request=request)
    products = PurchasedItem.objects.all()
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}")
    
    context={ 'purchasedItemsList' : products, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, "admin/store/purchaseditem/admin_purchased_item_list.html", context)


def soldItemList(request):
    cookieData = cartData(request=request)
    products = SoldItem.objects.all()
    print(f"........STORE PAGE......  noOfCartItems = {cookieData['noOfCartItems']}")
          
    context={ 'soldItemsList' : products, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, "admin/store/solditem/admin_sold_item_list.html", context)