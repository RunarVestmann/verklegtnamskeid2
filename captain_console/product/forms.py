from django.forms import ModelForm, widgets
from django import forms
from product.models import Product


class ProductForm(ModelForm):
    image = forms.ImageField()
    class Meta:
        model = Product
        exclude = ['id']
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'quantity': widgets.NumberInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control'}),
            'system': widgets.Select(attrs={'class': 'form-control'}),
            'release_date': widgets.SelectDateWidget(attrs={'class': 'form-control'}),
            'shop_arrival_date': widgets.SelectDateWidget(attrs={'class': 'form-control'})
        }