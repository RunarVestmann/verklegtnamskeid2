from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    username = forms.CharField(max_length=150)
    username.label = 'Notendanafn'

    first_name = forms.CharField(max_length=30)
    first_name.label = 'Fornafn'
    first_name.required = False
    last_name = forms.CharField(max_length=150)
    last_name.label = 'Eftirnafn'
    last_name.required = False
    email = forms.EmailField(max_length=254)
    email.label = 'Netfang'



    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

