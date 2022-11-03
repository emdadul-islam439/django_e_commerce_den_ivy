import json
from django.http import JsonResponse
from store.models import Order, OrderItem, Product, Cart, CartItem
from django.views.generic import DetailView
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
        self.cookieData = cartData(request = request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.order_id = self.kwargs.get('pk')
        self.items = OrderItem.objects.filter(order__id = self.order_id)
        self.products = Product.objects.all()
        
        orders = Order.objects.filter(id = self.order_id)
        self.trackInfoList = getTrackInfoList(orders[0].order_status)
        
        
        print(f'.............................order_id = {self.order_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
        return super(AdminOrderDetailView, self).get(request, *args, **kwargs) 
    
    
# @csrf_exempt
def updateAdminOrderStatus(request, **kwargs):
    data = json.loads(request.body)
    
    orderId = data['orderID']
    statusIdx = data['statusIdx']
    
    print(f"orderId = {orderId} ")
    print(f"statusIdx = {statusIdx}")
    
    order = Order.objects.get(id = orderId)
    
    order.order_status = statusIdx
    response_message = 'order_status CHANGED successfully'
    order.save()
    
    return JsonResponse(response_message, safe=False)  


# @csrf_exempt
def updateAdminOrderItem(request, **kwargs):
    data = json.loads(request.body)
    
    itemId = data['itemId']
    action = data['action']
    
    print('in UPDATE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {itemId} ")
    print(f"action = {action}")
    
    orderItem = OrderItem.objects.get(id = itemId)
    
    if action == 'add':
        orderItem.quantity += 1
        response_message = 'orderItem was INCREASED successfully'
    elif action == 'remove':
        if orderItem.quantity > 1:
            orderItem.quantity -= 1
            response_message = 'orderItem was DECREASED successfully'
        else:
            response_message = 'Failed! Only one item left!'
    
    orderItem.save()
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def removeAdminOrderItem(request, **kwargs):
    data = json.loads(request.body)
    
    itemId = data['itemId']
    
    order_id = kwargs.get('pk')
    items = OrderItem.objects.filter(order__id = order_id)
    itemCount = len(items)
    
    print('in REMOVE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {itemId} order_id = {order_id}  itemCount = {itemCount}")
    
    if itemCount > 1:
        orderItem = OrderItem.objects.get(id = itemId)
        orderItem.delete()
        response_message = 'orderItem was REMOVED successfully'
    else:
        response_message = 'Failed! Only one item left!'
        
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def addAdminOrderItems(request, **kwargs):
    data = json.loads(request.body)
    
    productIdList = data['productIdList']
    order_id = kwargs.get('pk')
    order = Order.objects.get(id=order_id)
    print(f"order_id = {order_id}  productIdList = {productIdList}")
    try:
        for productId in productIdList:
            product = Product.objects.get(id = productId)
            orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
            if orderItem.quantity == 0:
                orderItem.quantity = 1
                orderItem.save()
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
        self.cookieData = cartData(request = request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.cart_id = self.kwargs.get('pk')
        self.items = CartItem.objects.filter(cart__id = self.cart_id)
        self.products = Product.objects.all()
        
        print(f'.............................cart_id = {self.cart_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
        return super(AdminCartDetailView, self).get(request, *args, **kwargs) 
    
    
    
# @csrf_exempt
def updateAdminCartItem(request, **kwargs):
    data = json.loads(request.body)
    
    itemId = data['itemId']
    action = data['action']
    
    print('in UPDATE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {itemId} ")
    print(f"action = {action}")
    
    cartItem = CartItem.objects.get(id = itemId)
    
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
    
    cartItem.save()
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def removeAdminCartItem(request, **kwargs):
    data = json.loads(request.body)
    
    itemId = data['itemId']
    
    cart_id = kwargs.get('pk')
    items = CartItem.objects.filter(cart__id = cart_id)
    itemCount = len(items)
    
    print('in REMOVE-ADMIN-ORDER-ITEM().............')
    print(f"itemId = {itemId} cart_id = {cart_id}  itemCount = {itemCount}")
    
    cartItem = CartItem.objects.get(id = itemId)
    cartItem.delete()
    response_message = 'cartItem was REMOVED successfully'
        
    return JsonResponse(response_message, safe=False)


# @csrf_exempt
def addAdminCartItems(request, **kwargs):
    data = json.loads(request.body)
    
    productIdList = data['productIdList']
    cart_id = kwargs.get('pk')
    cart = Cart.objects.get(id=cart_id)
    print(f"cart_id = {cart_id}  productIdList = {productIdList}")
    try:
        for productId in productIdList:
            product = Product.objects.get(id = productId)
            cartItem, created = CartItem.objects.get_or_create(cart = cart, product = product)
            if cartItem.quantity == 0:
                cartItem.quantity = 1
                cartItem.save()
        response_message = f'{len(productIdList)} cartItem(s) ADDED successfully'
    except:
        response_message = 'Failed! Error occured while adding item!'
        
    return JsonResponse(response_message, safe=False)