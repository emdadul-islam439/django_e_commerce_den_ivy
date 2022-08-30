import json
from urllib import response
from django.shortcuts import render
from store.models import Order, Product, OrderItem, ShippingAddress
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        noOfCartItems = order.get_number_of_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_number_of_items': 0,
            'shipping': False
        }
        noOfCartItems = order['get_number_of_items']
        
    products = Product.objects.all()
    context={ 'products' : products, 'noOfCartItems':  noOfCartItems }
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        noOfCartItems = order.get_number_of_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_number_of_items': 0,
            'shipping': False
        }
        noOfCartItems = order['get_number_of_items']
    
    context={ 'items': items, 'order': order, 'noOfCartItems':  noOfCartItems }
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        noOfCartItems = order.get_number_of_items
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_number_of_items': 0,
            'shipping': False
        }
        noOfCartItems = order['get_number_of_items']
    
    context={ 'items': items, 'order': order, 'noOfCartItems':  noOfCartItems }
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
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    
    if action == 'add':
        orderItem.quantity += 1
        response_message = 'Item was ADDED successfully'
    elif action == 'remove':
        orderItem.quantity -= 1
        response_message = 'Item was DELETED successfully'
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse(response_message, safe=False)



def processOrder(request):
    print('Data: ', request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
        
    else:
        print('User is not authenticated....')
    return JsonResponse('Payment Completed...', safe=False)
    