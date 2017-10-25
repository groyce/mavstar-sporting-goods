from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.forms.forms import Form
from .forms import *


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'sports/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products}) 


def product_detail(request, id, slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'sports/product/detail.html',
                  {'product': product,'categories': categories,
                   'cart_product_form': cart_product_form})
    

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username =  form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('sports:product_list')
    return render(request, 'registration/login_form.html', {'form':form, 'title':title})


def register_view(request):
    title = 'Register'
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('sports:product_list')
    
    context = {
        "form":form,
        "title": title        
        }
    return render(request, "registration/login_form.html", context)


def logout_view(request):
    logout(request)
    return redirect('sports:product_list')

