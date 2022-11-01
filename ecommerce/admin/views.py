from django.shortcuts import render
from store.models import Order, OrderItem
from django.views.generic import DetailView
from store.utils import cartData, getWishListItems, getTrackInfoList

class AdminOrderDetailView(DetailView):
    login_required = True
    template_name: str = "admin/store/order/admin_order_details.html"
    context_object_name: str = "order"
    model = Order
    
    def get_context_data(self,*args, **kwargs):
        context = super(AdminOrderDetailView, self).get_context_data(*args,**kwargs)
        context['items'] = self.items
        context['noOfCartItems'] = self.noOfCartItems
        context['trackInfoList'] = self.trackInfoList
        return context
    
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request = request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.order_id = self.kwargs.get('pk')
        self.items = OrderItem.objects.filter(order__id = self.order_id)
        
        orders = Order.objects.filter(id = self.order_id)
        self.trackInfoList = getTrackInfoList(orders[0].order_status)
        
        
        print(f'.............................order_id = {self.order_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
        return super(AdminOrderDetailView, self).get(request, *args, **kwargs)   