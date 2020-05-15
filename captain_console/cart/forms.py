from django import forms
from creditcards.forms import CardNumberField, SecurityCodeField
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils.translation import gettext_lazy as _


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
    house_nbr.label = 'Húsnúmer'

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


class PaymentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Fullt nafn korthafa'}),
        required=True, max_length=100)
    card_nbr = CardNumberField(label='Kortanúmer')
    card_nbr.error_messages = {'invalid': 'Vinsamlegast sláðu inn gilt kortanúmer'}

    months = [
        ('01', '01'), ('02', '02'),('03', '03'),('04', '04'),('05', '05'),('06', '06'),
        ('07', '07'),('08', '08'),('09', '09'),('10', '10'),('11', '11'),('12', '12')
    ]
    # We set the current month as the default value in the exp_month field
    initial_month = datetime.now().month
    if initial_month < 10:
        initial_month = '0' + str(initial_month)
    exp_month = forms.ChoiceField(choices=months, initial=initial_month, widget=forms.Select(attrs={'class': 'form-control'}))
    exp_month.label = 'Gildistími'

    year = datetime.now().year
    years = []
    # We only show 5 years in the exp_year field since credit cards expire within that timerange
    for i in range(5):
        years.append((str(year + i), str(year + i)[2:]))
    exp_year = forms.ChoiceField(choices=years, initial=year, widget=forms.Select(attrs={'class': 'form-control'}))
    exp_year.label = 'Gildisár'

    cvc_nbr = SecurityCodeField(label='CVV/CVC', min_length=3, max_length=4)
    cvc_nbr.error_messages = {'invalid': 'Vinsamlegast sláðu inn gilt CVC númer'}


    def clean(self):
        exp_month = self.cleaned_data['exp_month']
        exp_year = self.cleaned_data['exp_year']

        # For see if the user inputs a date that is less than the current date
        if int(exp_year) == int(datetime.now().year):
            if int(exp_month) < int(datetime.now().month):
                raise ValidationError(_('Gildistími er liðinn'), code='invalid')
        return self.cleaned_data
