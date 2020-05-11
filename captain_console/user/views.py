from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import SignUpForm
from .profile_form import ProfileForm
from django.shortcuts import render, redirect
from .models import Profile, Search
from product.models import Product

import json

# Create your views here.
def index(request):
    return render(request, 'user/user.html')

# sometest to put singup and login in tabs
# result so far login crash everyting problem with reload sign up if not success

# def index(request):
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#         form.save()
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password1')
#         user = authenticate(username=username, password=password)
#         login(request, user)
#         return redirect('user')
#     return render(request, 'user/user.html', {'form': form})



def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        profile = Profile()
        profile.user = request.user
        profile.save()
        return redirect('home')

    return render(request, 'user/signup.html', {'form': form})


    # def login_view(request):
    #     form = LoginForm(request, data=request.POST)
    #
    #     if form.is_valid():
    #         username = form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password')
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         return redirect('home')
    #
    #     return render(request, 'user/login.html', {'form': form})


@login_required
def profile(request):
    user_profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ProfileForm(instance=profile, data=request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('profile')
    return render(request, 'user/profile.html', {'form': ProfileForm(instance=user_profile)})


@login_required
def viewed_products(request):
    user_id = request.user.id
    return render(request, 'user/viewed_products.html', {
        'products': get_product_list(user_id)
    })

search_list = []

def add_to_search(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            try:
                user_profile = Profile.objects.get(user__id=request.user.id)
            # The user has no profile so we create one
            except Profile.DoesNotExist:
                user_profile = Profile()
                user_profile.user = request.user
                user_profile.save()

            search = Search()
            search.profile = user_profile

            try:
                product_id = json.loads(request.body)
            except json.JSONDecodeError:
                return send_json('JSON was invalid', 400)

            if (user_profile.id, product_id) in search_list:
                return send_json('The search already exists', 409)
            elif Search.objects.filter(profile__id=user_profile.id, product__id=product_id).exists():
                search_list.remove((user_profile.id, product_id))
                return send_json('The search already exists', 409)
            else:
                search_list.append((user_profile.id, product_id))
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return send_json('The viewed product was not found', 404)

            search.product = product
            search.save()
            return send_json('', 201, product_id)
    else:
        return send_json('Request method not supported', 400)

def send_json(message, status_code, data={}):
    response = JsonResponse({
        'data': data,
        'message': message
    })
    response.status_code = status_code
    return response

# Get a list of all the products the current user has viewed
def get_product_list(user_id):
    search = Search.objects.filter(profile__user_id=user_id).values_list('product_id', flat=True)
    product_list = []
    for i in search:
        curr_product = Product.objects.get(id=i)
        product_list.append(curr_product)
    return product_list