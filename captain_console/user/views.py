from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from .models import Profile, Search
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
    #mostly to test login_requried decorator
    return render(request, 'user/profile.html')

@login_required
def viewed_products(request):
    return render(request, 'user/viewed_products.html', {
        'search': Search.objects.filter(profile=request.user.id)
    })


def add_to_search(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            profile = Profile.objects.filter(user=request.user)
            search = Search()
            search.profile = profile
            data = json.loads(request.body)
            search.product = data.productId
            search.save()
    else:
        response = JsonResponse({
            'data': {},
            'message': 'Request method not supported'
        })
        response.status_code = 400
        return response