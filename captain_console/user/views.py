from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    return render(request, 'user/user.html')


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'user/registration.html', {
        # included django form
        'form': UserCreationForm()
    })

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'user/signup.html', {'form': form})


@login_required
def profile(request):
    #mostly to test login_requried decorator
    return render(request, 'user/profile.html')
