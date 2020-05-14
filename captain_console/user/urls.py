from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

from .forms import LoginForm




urlpatterns = [
    # http://localhost:8000/user  -> render profil or redirect to login
    path('', views.profile, name='user'),

    # http://localhost:8000/user/login
    path('login', views.login_view, name='login'),

    # http://localhost:8000/user/logout -> redirect to login
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),

    # http://localhost:8000/user/profile
    path('profile', views.profile, name='profile'),

    # http://localhost:8000/user/signup
    path('signup', views.signup_view, name='signup'),

    # http://localhost:8000/user/viewed_products -> if login
    path('viewed_products', views.viewed_products, name='viewed_products'),

    # http://localhost:8000/user/add_to_search -> json
    path('add_to_search', views.add_to_search, name='add_to_search'),

]

