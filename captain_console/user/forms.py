from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    username.label = 'Notandanafn'

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=30)
    first_name.label = 'Fornafn'
    first_name.required = False
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    last_name.label = 'Eftirnafn'
    last_name.required = False
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=254)
    email.label = 'Netfang'

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password1.label = 'Lykilorð'
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2.label = 'Staðfesting lykilorðs'
    password2.error_messages = {'required' : 'Veljið lykilorð sem er að lágmarki 8 stafir'}


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))