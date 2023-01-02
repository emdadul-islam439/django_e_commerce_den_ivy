from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView

from customers.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from store.utils import cartData, getWishListItems, getTrackInfoList, getCartItemList, getStockInfoList
from store.models import Order, OrderItem
from customers.models import AdminUser

# Create your views here.
def redirectUser(request):
    print('IN RE-DIRECT-USER')
    admin_users = AdminUser.objects.all()
    print(f'admin_users = {admin_users}')
    
    for admin in admin_users:
        print(f'admin.id = {admin.id} request.user.id = ', request.user.id)
        if request.user.id == admin.id:
            return redirect('admin/store/stock/', permanent=True)
    return redirect('store/', parmanent=True)
    
    
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully! You can now login into your account.")
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "customers/register.html", {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, 
                                instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES, 
                                   instance=request.user.customer)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your account has been updated successfully!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)
    
    cookieData = cartData(request=request)
    noOfCartItems = cookieData['noOfCartItems']
    context = {
        "u_form" : u_form,
        "p_form" : p_form,
        "noOfCartItems" : noOfCartItems
    }
    return render(request, "customers/profile.html", context)
     
    
def wishList(request):
    cookieData = cartData(request=request)
    products = getWishListItems(request)
    cartItemList = getCartItemList(request, products, cookieData)
    stockInfoList = getStockInfoList(products)
    productInfoList = list(zip(products, cartItemList, stockInfoList))
    
    context = { 'productInfoList' : productInfoList, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, 'customers/wishlist.html', context)
    

@login_required 
def orderList(request):
    cookieData = cartData(request=request)
    orders = Order.objects.order_by('-id').filter(customer = request.user.customer)
    print('in orderList()------> ORDERS: ', orders)
    
    context={ 'orders' : orders, 'noOfCartItems':  cookieData['noOfCartItems']}
    return render(request, 'customers/order-list.html', context)


class OrderDetailView(DetailView):
    login_required = True
    template_name: str = "customers/order-details.html"
    context_object_name: str = "order"
    model = Order
    
    def get_context_data(self,*args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args,**kwargs)
        context['items'] = self.items
        context['noOfCartItems'] = self.noOfCartItems
        context['trackInfoList'] = self.trackInfoList
        return context
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request=request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.order_id = self.kwargs.get('pk')
        self.items = OrderItem.objects.filter(order__id=self.order_id)
        
        order = Order.objects.filter(id=self.order_id).first()
        
        if order.order_status == 5:
            return redirect('/order-list/')
        else:
            self.trackInfoList = getTrackInfoList(order.order_status)
            print(f'order_id = {self.order_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
            return super(OrderDetailView, self).get(request, *args, **kwargs)   
