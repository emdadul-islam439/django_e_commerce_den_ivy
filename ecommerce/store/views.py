from django.shortcuts import render
from store.models import Order, Product
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def store(request):
    products = Product.objects.all()
    context={ 'products' : products }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_number_of_items': 0
        }
    
    context={ 'items': items, 'order': order }
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total': 0,
            'get_number_of_items': 0
        }
    
    context={ 'items': items, 'order': order }
    return render(request, 'store/checkout.html', context)

# @csrf_exempt
def UpdateItem(request):
    return JsonResponse('Item was added', safe=False)