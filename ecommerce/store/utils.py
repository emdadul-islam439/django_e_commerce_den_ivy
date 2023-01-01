import json
from math import prod

from . models import *

def cookieCart(request):
    try:
        temp_cart = json.loads(request.COOKIES['cart'])
    except:
        temp_cart = {}
            
    print('temp_cart: ', temp_cart)
    items = []
    cart = {
        'get_cart_total': 0,
        'get_checked_item_count': 0,
        'shipping': False
    }
    noOfCartItems = 0
    
    for id in temp_cart:
        try:
            noOfCartItems += temp_cart[id]['quantity']

            product = Product.objects.get(id=id)
            total = (product.price * temp_cart[id]['quantity'])
            
            if temp_cart[id]['is_checked']:
                cart['get_cart_total'] += total
                cart['get_checked_item_count'] += temp_cart[id]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': temp_cart[id]['quantity'],
                'get_total': total,
                'is_checked': temp_cart[id]['is_checked']
            }
            items.append(item)

            if product.digital == False:
                cart['shipping'] = True 
        except:
            pass
    
    return {
        'noOfCartItems': noOfCartItems, 
        'cart': cart, 
        'items': items
    }
    

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        noOfCartItems = cart.get_all_cart_item_count
    else:
        cookieData = cookieCart(request=request)
        noOfCartItems = cookieData['noOfCartItems']
        cart = cookieData['cart']
        items = cookieData['items']
    
    return {
        'noOfCartItems': noOfCartItems, 
        'cart': cart, 
        'items': items
    }
    
    
def guestOrder(request, data):
    print('User is not authenticated....')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    
    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name 
    customer.save(update_fields=['name'])
    
    cart = Cart.objects.create(customer=customer)
    
    cookieData = cookieCart(request=request)
    items = cookieData['items']
    for item in items:
        if item['is_checked'] == False: 
            continue
        
        product = Product.objects.get(id=item['product']['id'])
        cartItem = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=item['quantity']
        )

    return customer, cart


def getWishListItems(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        wishListInfo = customer.wishlistitem_set.all()
        wishListProducts = []
        for wishListItem in wishListInfo:
            wishListProducts.append(wishListItem.product)
        print(f'wishListProducts  =  {wishListProducts}')
    else:
        wishListProducts = []
    
    return wishListProducts


def getTrackInfoList(order_status: int):
    class TrackItem:
        def __init__(self, title: str, is_completed: bool, icon: str):
            self.title = title
            self.is_completed = is_completed
            self.icon = icon
    
    title_tuple = (
        'Waiting for Payment', 
        'Preparing Order', 
        'Order is Prepared', 
        'Order in Shipping', 
        'Order is Delivered',
    )
    icon_tuple = (
        'pe-7s-timer',
        'pe-7s-note',
        'pe-7s-note2',
        'pe-7s-plane',
        'pe-7s-check'
    )
    
    i = 0
    track_info_list = []
    length = len(title_tuple)
    while i < length:
        is_completed = i <= order_status
        track_info_list.append(TrackItem(title_tuple[i], is_completed, icon_tuple[i]))
        i += 1
        
    print(f'from GET-TRACK-INFO-LIST..... track_info_list[0] = {track_info_list[0].title}, {track_info_list[0].is_completed}, {track_info_list[0].icon}')
    return track_info_list


def getCartItemList(request, products, cookieData):
    cartItemList = []
    cartItems = cookieData['items']
    
    for product in products:
        isNotFound = True
        for item in cartItems:
            if isSame(request, product, item):
                isNotFound = False
                cartItemList.append({ 'quantity': getQuantity(request, item) })
                break
        if isNotFound:
            cartItemList.append({ 'quantity': 0 })
            
    return cartItemList


def isSame(request, product, item):
    if request.user.is_authenticated:
        return product == item.product
    else:
        return product.id == item['product']['id']
    
    
def getQuantity(request, item):
    if request.user.is_authenticated:
        return item.quantity
    else:
        return item['quantity']


def getStockInfoList(products):
    stockInfoList = []
    
    for product in products:
        stockItem = Stock.objects.filter(product=product.id).first()
        if stockItem is not None:
            stockInfoList.append({ 'effectiveOrderLimit': stockItem.effective_order_limit })
        else:
            stockInfoList.append({ 'effectiveOrderLimit': 0 })
            
    return stockInfoList


def getProductListFromCartItems(request, items):
    productList = []
    
    for item in items:
        if request.user.is_authenticated:
            productList.append(item.product) 
        else:
            product = Product.objects.get(id=item['product']['id'])
            productList.append(product)
            
    return productList