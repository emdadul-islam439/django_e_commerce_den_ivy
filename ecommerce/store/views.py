import json
from urllib import response
from django.shortcuts import render
from store.models import Order, Product, OrderItem, ShippingAddress, Customer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from . utils import cartData, guestOrder, cookieCart

# Create your views here.
def store(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
        
    products = Product.objects.all()
    context={ 'products' : products, 'noOfCartItems':  noOfCartItems }
    return render(request, 'store/store.html', context)


def cart(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
    order = cookieData['order']
    items = cookieData['items']
    
    context={ 'items': items, 'order': order, 'noOfCartItems':  noOfCartItems }
    return render(request, 'store/cart.html', context)


def checkout(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
    order = cookieData['order']
    items = cookieData['items']
    
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
    print(f"Data : {data}")
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
    else:
        customer, order = guestOrder(request= request, data= data)
        
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
    return JsonResponse('Payment Completed...', safe=False)
    