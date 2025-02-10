from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
from cart.cart import Cart
import json
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404


# Create your views here.

def search(request):
    # Determine if they filled out the search form
    if request.method == "POST":
        searched = request.POST['searched']

        # Query The Product DB Model
        searched = Product.objects.filter(Q(name__icontains=searched)  | Q(description__icontains=searched))
        if not searched:
            messages.success(request, 'Sorry, The Product You Searched For Does Not Exist. Please Try Again')
            return render(request, 'search.html', {})
        
        else:
            return render(request, 'search.html', {'searched': searched})   

    return render(request, 'search.html', {})



def update_info(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get Current User's Shipping Info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)

        

        # Get original User Form
        form = UserInfoForm(request.POST or None, instance=current_user)

        # Get User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():

            # Original form saved
            form.save()

            # Shipping form saved
            shipping_form.save()

        
            messages.success(request, 'Your Info Has Been Updated!')
            return redirect('home')
        return render(request, "update_info.html", {'form': form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!")
        return redirect('home')

def update_password(request):

    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            # Do something
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your Password Has Been Updated')
                login(request, current_user)
                return redirect('login')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')

        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, 'You Must Be Logged In To View That Page')
        return redirect('home')

    # return render(request, "update_password.html", {})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'User Profile Has Been Updated!')
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form})
    else:
        messages.success(request, "You Must Be Logged In To Access That Page!")
        return redirect('home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})


def category(request, foo):
    # Replace Spaces with Hypens
    foo = foo.replace('-', ' ')

    # Grab the category from the url
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {"products": products, 'category': category})
    except:
        messages.error(request, ('That Category does not exist'))
        return redirect('home')


# Products
def product(request, pk):
    try:
        product = get_object_or_404(Product, id=pk)
        # Get related products from the same category, excluding the current product
        related_products = Product.objects.filter(category=product.category).exclude(id=pk).order_by('?')[:4]
        return render(request, 'product.html', {
            'product': product,
            'related_products': related_products,
            'categories': Category.objects.all()
        })
    except Http404:
        messages.error(request, "Product not found.")
        return redirect('home')
    except Exception as e:
        print(f"Error in product view: {str(e)}")
        return render(request, '500.html', status=500)


def home(request):
    try:
        products = Product.objects.all()
        categories = Category.objects.all()
        return render(request, 'home.html', {
            'products': products,
            'categories': categories
        })
    except Exception as e:
        # Log the error for debugging
        print(f"Error in home view: {str(e)}")
        # Return a friendly error page
        return render(request, '500.html', status=500)


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    current_user = Profile.objects.get(user__id=request.user.id)
                    # Get their saved cart from the database
                    saved_cart = current_user.old_cart
                    # Convert database string to python dictionary(original cart format)
                    if saved_cart:
                        # Convert to dictionary using JSON
                        converted_cart = json.loads(saved_cart)
                        # Add the loaded cart dictionary to our session
                        cart = Cart(request)
                        # Loop thru the cart and add the items from the database
                        for key,value in converted_cart.items():
                            cart.db_add(product=key, quantity=value)
                except (Profile.DoesNotExist, json.JSONDecodeError) as e:
                    print(f"Error loading saved cart: {str(e)}")
                    # Continue without loading saved cart
                    pass

                messages.success(request, "Login successful")
                return redirect('home')
            else:
                messages.error(request, "Login failed, please try again")
                return redirect('login')
        except Exception as e:
            print(f"Error in login view: {str(e)}")
            messages.error(request, "An error occurred during login")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out successfully'))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, ('You have been Registered successfully! Welcome!'))
            return redirect('home')
        else:
            messages.error(
                request, ('Whoops! There was a problem registering! Please try again'))
            return redirect('register')

    else:
        return render(request, 'register.html', {'form': form})
