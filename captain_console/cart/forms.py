from django import forms
from creditcards.forms import CardExpiryField, CardNumberField, SecurityCodeField
from django.forms import Widget


class ShippingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Fullt nafn'}),
                           required=True, max_length=100)
    name.label = 'Nafn'
    name.error_messages = {'required': 'Vinsamlega sláðu inn nafn'}

    street_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Heimilisfang'}),
                                 required=True, max_length=100)
    street_name.label = 'Heimilisfang'
    street_name.error_messages = {'required': 'Vinsamlega sláðu inn götuheiti'}

    house_nbr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Húsnúmer'}),
                                required=False, max_length=100)
    house_nbr.label = 'Húsnúmer '

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Staður'}),
                           required=True, max_length=100)
    city.label = 'Staður'
    city.error_messages = {'required': 'Vinsamlega sláðu inn stað '}

    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Póstnúmer'}),
                               required=True, max_length=100)
    zip_code.label = 'Póstnúmer'
    zip_code.error_messages = {'required': 'Vinsamlega sláðu inn póstnúmer'}

    countries = [('AFG', 'Afganistan'),('USA', 'Bandaríkin'),('FRA', 'Frakkland'),('GRE', 'Grænland'),('ISL', 'Ísland'), ('NOR', 'Noregur'),('XXX', 'Annarstaðar')]

    country = forms.ChoiceField(choices=countries, initial='ISL', widget=forms.Select(attrs={'class': 'form-control'}))
    country.label = 'Land'
    country.error_messages = {'required': 'Vinsamlega veldu land'}


# class PaymentForm(forms.Form):
#     name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
#                                                          'placeholder': 'Fullt nafn korthafa'}),
#                            required=True, max_length=100)
#     name.label = 'Nafn'
#     name.error_messages = {'required': 'Vinsamlegast sláðu inn nafn'}
#
#     card_nbr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
#                                                                'placeholder': 'Kortanúmer'}),
#                                  required=True, max_length=16, min_length=16)
#     card_nbr.label = 'Kortanúmer'
#     card_nbr.error_messages = {'required': 'Vinsamlegast sláðu inn kortanúmer'}
#
#
#     exp_day = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
#                                                                'placeholder': 'Gildistími(MM/YY)'}),
#                                  required=True, max_length=16)
#     exp_day.label = 'Gildistími'
#     exp_day.error_messages = {'required': 'Vinsamlegast sláðu inn gildistíma'}
#
#     cvc_nbr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
#                                                               'placeholder': 'Öryggisnúmer'}),
#                                 required=False, max_length=3, min_length=3)
#     cvc_nbr.label = 'CVC '
#     cvc_nbr.error_messages = {'required': 'Vinsamlegast sláðu inn öryggisnúmerið '}

class PaymentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Fullt nafn korthafa'}),
        required=True, max_length=100)
    card_nbr = CardNumberField(label='Kortanúmer')
    card_nbr.error_messages = {'invalid': 'Vinsamlegast sláðu inn gilt kortanúmer'}
    exp_day = CardExpiryField(label='Gildistími')
    cvc_nbr = SecurityCodeField(label='CVV/CVC')