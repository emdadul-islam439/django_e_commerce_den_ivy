from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from customers.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from store.utils import cartData, getWishListItems

# Create your views here.
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
    
    
def orderList(request):
    # cookieData = cartData(request = request)
    # noOfCartItems = cookieData['noOfCartItems']
        
    # products = getWishListItems(request)
    # # products = Product.objects.all()
    # print('PRODUCTs: ', products)
    # context={ 'products' : products, 'noOfCartItems':  noOfCartItems}
    return render(request, 'customers/order-list.html')