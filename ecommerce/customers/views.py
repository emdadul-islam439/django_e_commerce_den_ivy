from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customers.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from store.utils import cartData, getWishListItems
from store.models import Cart, CartItem
from customers.models import AdminUser
from django.views.generic import DetailView
from store import views as store_views


# Create your views here.
def redirectUser(request):
    print('IN RE-DIRECT-USER')
    admin_users = AdminUser.objects.all()
    print(f'admin_users = {admin_users}')
    
    for admin in admin_users:
        print(f'admin.id = {admin.id}')
        print('request.user.id = ', request.user.id)
        if request.user.id == admin.id:
            return redirect('admin/', permanent= True)
    return redirect('store/', parmanent= True)
    
    

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created successfully! You can now login into your account.")
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
            messages.success(request, f"Your account has been updated successfully!")
            return redirect('profile')
            
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)
    
    
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
    context = {
        "u_form" : u_form,
        "p_form" : p_form,
        "noOfCartItems" : noOfCartItems
    }
    
    return render(request, "customers/profile.html", context)
     
    
def wishList(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
        
    products = getWishListItems(request)
    # products = Product.objects.all()
    print('PRODUCTs: ', products)
    context={ 'products' : products, 'noOfCartItems':  noOfCartItems}
    return render(request, 'customers/wishlist.html', context)
    # return HttpResponse("HI, this is the wishlist page")
    

@login_required 
def orderList(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
        
    orders = Cart.objects.order_by('-id').filter(customer = request.user.customer)
    # orders.sort(key=attrgetter('id'), reverse=True)
    print('ORDERS: ', orders)
    context={ 'orders' : orders, 'noOfCartItems':  noOfCartItems}
    return render(request, 'customers/order-list.html', context)
    

def orderDetails(request):
    cookieData = cartData(request = request)
    noOfCartItems = cookieData['noOfCartItems']
        
    orders = Cart.objects.order_by('-id').filter(customer = request.user.customer)
    # orders.sort(key=attrgetter('id'), reverse=True)
    print('ORDERS: ', orders)
    context={ 'orders' : orders, 'noOfCartItems':  noOfCartItems}
    return render(request, 'customers/order-list.html', context)


class OrderDetailView(DetailView):
    template_name: str = "customers/order-details.html"
    context_object_name: str = "order"
    model = Cart
    
    def get_context_data(self,*args, **kwargs):
        context = super(OrderDetailView, self).get_context_data(*args,**kwargs)
        context['items'] = self.items
        context['noOfCartItems'] = self.noOfCartItems
        return context
    
    
    def get(self, request, *args, **kwargs):
        self.cookieData = cartData(request = request)
        self.noOfCartItems = self.cookieData['noOfCartItems']
        self.order_id = self.kwargs.get('pk')
        self.items = CartItem.objects.filter(order__id = self.order_id)
        
        
        print(f'order_id = {self.order_id}  items = {self.items},  noOfCartItems = {self.noOfCartItems}')
        return super(OrderDetailView, self).get(request, *args, **kwargs)   