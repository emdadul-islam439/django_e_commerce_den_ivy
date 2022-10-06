import json
from math import prod
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
            
    print('Cart: ', cart)
    items = []
    cart = {
        'get_cart_total': 0,
        'get_number_of_items': 0,
        'shipping': False
    }
    noOfCartItems = cart['get_number_of_items']
    
    for id in cart:
        try:
            noOfCartItems += cart[id]['quantity']

            product = Product.objects.get(id= id)
            total = (product.price * cart[id]['quantity'])

            cart['get_cart_total'] += total
            cart['get_number_of_items'] += cart[id]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL
                },
                'quantity': cart[id]['quantity'],
                'get_total': total
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
        cart, created = Cart.objects.get_or_create(customer = customer, complete = False)
        items = cart.cartitem_set.all()
        noOfCartItems = cart.get_number_of_items
    else:
        cookieData = cookieCart(request = request)
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
    
    
    cookieData = cookieCart(request= request)
    items = cookieData['items']
    
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name 
    customer.save()
    
    cart = Cart.objects.create(
        customer = customer,
        complete = False
    )
    
    for item in items:
        product = Product.objects.get(id= item['product']['id'])
        
        cartItem = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = item['quantity']
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
        