import json
from django.http import JsonResponse
from django.views.generic import DetailView

from store.models import Order, OrderItem, Product, Cart, CartItem
from store.utils import cartData, getTrackInfoList

class AdminOrderDetailView(DetailView):
    login_required = True
    template_name: str = "admin/store/order/admin_order_details.html"
    context_object_name: str = "order"
    model = Order
    
    def get_context_data(self,*args, **kwargs):
        context = super(AdminOrderDetailView, self).get_context_data(*args,**kwargs)
        context['items'] = self.items
        context['products'] = self.products
        context['noOfCartItems'] = self.noOfCartItems
        context['trackInfoList'] = self.trackInfoList
        return context
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request=request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.order_id = self.kwargs.get('pk')
        self.items = OrderItem.objects.filter(order__id=self.order_id)
        self.products = Product.objects.all()
        
        orders = Order.objects.filter(id=self.order_id)
        self.trackInfoList = getTrackInfoList(orders[0].order_status)
        
        print(f'.............................order_id = {self.order_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
        return super(AdminOrderDetailView, self).get(request, *args, **kwargs) 
    
    
# @csrf_exempt
def updateAdminOrderStatus(request, **kwargs):
    data = json.loads(request.body)
    print('in UPDATE-ADMIN-ORDER-STATUS().............')
    print(f"orderId = {data['orderID']} statusIdx = {data['statusIdx']}")
    
    Order.objects.filter(id=data['orderID']).update(order_status=data['statusIdx'])
    
    response_message = 'order_status CHANGED successfully'
    return JsonResponse(response_message, safe=False)  


# @csrf_exempt
def updateAdminOrderItem(request, **kwargs):
    data = json.loads(request.body)
    action = data['action']
    print('in UPDATE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {data['itemId']} action = {action}")
    
    orderItem = OrderItem.objects.get(id=data['itemId'])
    
    if action == 'add':
        orderItem.quantity += 1
        response_message = 'orderItem was INCREASED successfully'
    elif action == 'remove':
        if orderItem.quantity > 1:
            orderItem.quantity -= 1
            response_message = 'orderItem was DECREASED successfully'
        else:
            response_message = 'Failed! Only one item left!'
    orderItem.save(update_fields=['quantity'])
    
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def removeAdminOrderItem(request, **kwargs):
    data = json.loads(request.body)
    items = OrderItem.objects.filter(order__id=kwargs.get('pk'))
    print('in REMOVE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {data['itemId']} order_id = {kwargs.get('pk')}  itemCount = {len(items)}")
    
    if len(items) > 1:
        OrderItem.objects.filter(id=data['itemId']).delete()
        response_message = 'orderItem was REMOVED successfully'
    else:
        response_message = 'Failed! Only one item left!'
        
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def addAdminOrderItems(request, **kwargs):
    data = json.loads(request.body)
    
    productIdList = data['productIdList']
    order = Order.objects.get(id=kwargs.get('pk'))
    print(f"order_id = {kwargs.get('pk')}  productIdList = {productIdList}")
    try:
        for productId in productIdList:
            product = Product.objects.get(id=productId)
            orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
            if orderItem.quantity == 0:
                orderItem.quantity = 1
                orderItem.save(update_fields=['quantity'])
        response_message = f'{len(productIdList)} orderItem(s) ADDED successfully'
    except:
        response_message = 'Failed! Error occured while adding item!'
        
    return JsonResponse(response_message, safe=False)


class AdminCartDetailView(DetailView):
    login_required = True
    template_name: str = "admin/store/cart/admin_cart_details.html"
    context_object_name: str = "cart"
    model = Cart
    
    def get_context_data(self,*args, **kwargs):
        context = super(AdminCartDetailView, self).get_context_data(*args,**kwargs)
        context['items'] = self.items
        context['products'] = self.products
        context['noOfCartItems'] = self.noOfCartItems
        return context
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request=request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.cart_id = self.kwargs.get('pk')
        self.items = CartItem.objects.filter(cart__id=self.cart_id)
        self.products = Product.objects.all()
        
        print(f'.............................cart_id = {self.cart_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
        return super(AdminCartDetailView, self).get(request, *args, **kwargs) 
    
    
# @csrf_exempt
def updateAdminCartItem(request, **kwargs):
    data = json.loads(request.body)
    action = data['action']
    print('in UPDATE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {data['itemId']} action = {action}")
    
    cartItem = CartItem.objects.get(id = data['itemId'])
    
    if action == 'add':
        cartItem.quantity += 1
        response_message = 'cartItem was INCREASED successfully'
    elif action == 'remove':
        if cartItem.quantity > 1:
            cartItem.quantity -= 1
            response_message = 'cartItem was DECREASED successfully'
        else:
            response_message = 'Failed! Only one item left!'
    elif action == 'check-uncheck':
        cartItem.is_checked = not cartItem.is_checked
        response_message = 'Item was CHECKED/UNCHECKED successfully'
    
    cartItem.save(update_fields=['quantity', 'is_checked'])
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def removeAdminCartItem(request, **kwargs):
    data = json.loads(request.body)
    items = CartItem.objects.filter(cart__id=kwargs.get('pk'))
    print('in REMOVE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {data['itemId']} cart_id = {kwargs.get('pk')}  itemCount = {len(items)}")
    
    CartItem.objects.filter(id=data['itemId']).delete()
    response_message = 'cartItem was REMOVED successfully'
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def addAdminCartItems(request, **kwargs):
    data = json.loads(request.body)
    productIdList = data['productIdList']
    cart = Cart.objects.get(id=kwargs.get('pk'))
    print(f"cart_id = {kwargs.get('pk')}  productIdList = {productIdList}")
    try:
        for productId in productIdList:
            product = Product.objects.get(id = productId)
            cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if cartItem.quantity == 0:
                cartItem.quantity = 1
                cartItem.save(update_fields=['quantity'])
        response_message = f'{len(productIdList)} cartItem(s) ADDED successfully'
    except:
        response_message = 'Failed! Error occured while adding item!'
        
    return JsonResponse(response_message, safe=False)