import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
            
    print('Cart: ', cart)
    items = []
    order = {
        'get_cart_total': 0,
        'get_number_of_items': 0,
        'shipping': False
    }
    noOfCartItems = order['get_number_of_items']
    
    for id in cart:
        try:
            noOfCartItems += cart[id]['quantity']

            product = Product.objects.get(id= id)
            total = (product.price * cart[id]['quantity'])

            order['get_cart_total'] += total
            order['get_number_of_items'] += cart[id]['quantity']

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
                order['shipping'] = True 
        except:
            pass
    
    return {
        'noOfCartItems': noOfCartItems, 
        'order': order, 
        'items': items
    }