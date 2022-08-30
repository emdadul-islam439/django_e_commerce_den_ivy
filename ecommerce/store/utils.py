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
    

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        noOfCartItems = order.get_number_of_items
    else:
        cookieData = cookieCart(request = request)
        noOfCartItems = cookieData['noOfCartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    return {
        'noOfCartItems': noOfCartItems, 
        'order': order, 
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
    
    order = Order.objects.create(
        customer = customer,
        complete = False
    )
    
    for item in items:
        product = Product.objects.get(id= item['product']['id'])
        
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )

    return customer, order