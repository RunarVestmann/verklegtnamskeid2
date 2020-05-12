from django import forms


class ShippingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Settu inn fullt nafn hjá móttakanda'}),
                           required=True, max_length=100)
    name.label = 'Nafn'
    name.error_messages = {'required': 'Vinsamlega sláðu inn nafn'}

    street_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Settu inn götuheiti hjá móttakanda'}),
                                 required=True, max_length=100)
    street_name.label = 'Heimilisfang'
    street_name.error_messages = {'required': 'Vinsamlega sláðu inn götuheiti'}

    house_nbr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Settu inn húsnúmer eða önnur nauðsynleg einkenni'}),
                                required=False, max_length=100)
    house_nbr.label = 'Húsnúmer '
    house_nbr.error_messages = {'required': 'Vinsamlega sláðu inn húsnúmer '}

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Settu inn borg, bæ eða sveitafélag'}),
                           required=True, max_length=100)
    city.label = 'Staður'
    city.error_messages = {'required': 'Vinsamlega sláðu inn stað '}

    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Settu inn póstnúmer'}),
                               required=True, max_length=100)
    zip_code.label = 'Póstnúmer'
    zip_code.error_messages = {'required': 'Vinsamlega sláðu inn póstnúmer'}




    countries = [('AFG', 'Afganistan'),('USA', 'Bandaríkin'),('FRA', 'Frakkland'),('GRE', 'Grænland'),('ISL', 'Ísland'), ('NOR', 'Noregur'),('XXX', 'Annarstaðar')]

    country = forms.ChoiceField(choices=countries, initial='ISL', widget=forms.Select(attrs={'class': 'form-control'}))
    country.label = 'Land'
    country.error_messages = {'required': 'Vinsamlega veldu land'}




class PaymentForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'Settu inn nafnið sem er á greiðslukortinu'}),
                           required=True, max_length=100)
    name.label = 'Nafn'
    name.error_messages = {'required': 'Vinsamlega sláðu inn nafn'}

    card_nbr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Settu inn kortanúmer'}),
                                 required=True, max_length=16)
    card_nbr.label = 'Kortanúmer'
    card_nbr.error_messages = {'required': 'Vinsamlega sláðu inn kortanúmer'}


    exp_day = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Settu inn gildistíma mán/ár (00/00)'}),
                                 required=True, max_length=16)
    exp_day.label = 'Gildistími'
    exp_day.error_messages = {'required': 'Vinsamlega sláðu inn gildistíma'}



    cvc_nbr = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Settu inn öryggisnúmerið sem er aftan á kortinu'}),
                                required=False, max_length=10)
    cvc_nbr.label = 'CVC '
    cvc_nbr.error_messages = {'required': 'Vinsamlega sláðu inn öryggisnúmerið '}

