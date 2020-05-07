from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

from .forms import LoginForm




urlpatterns = [
    path('', views.index, name='user'),
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile', views.profile, name='profile'),
    path('signup', views.signup_view, name='signup'),






]

