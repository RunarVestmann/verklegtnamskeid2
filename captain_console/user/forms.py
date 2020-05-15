from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from user.models import Search
from .models import Profile
from string import Template
from django.utils.safestring import mark_safe
from django.forms import ImageField
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150, label='Notandanafn')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30, label='Fornafn', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150, label='Eftirnafn', required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=254, label='Netfang')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Lykilorð')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Staðfesting lykilorðs')
    #password2.error_messages = {'required': 'Veljið lykilorð sem er að lágmarki 8 stafir'}

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Lykilorð')

    class Meta:
        model = User
        fields = ('username', 'password' )

class ProfileForm(ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Notandanafn')
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Fornafn', required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Eftirnafn', required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Netfang')
    class Meta:
        model = Profile
        exclude = ['id', 'user', 'shopping_cart']
        field = ('image', 'username', 'first_name', 'last_name', 'email')

class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ['profile', 'product', 'date_of_search']

