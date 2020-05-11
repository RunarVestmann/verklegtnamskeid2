from django import forms
from django.core.validators import EmailValidator

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=100)
    name.label = 'Nafn'
    name.error_messages = {'required': 'Vinsamlega sláðu inn nafn'}
    from_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True,
                                  max_length=100, error_messages={'invalid': 'Sláðu inn gilt netfang'}, label='Netfang',validators=[EmailValidator(message="Skráðu email")])
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, max_length=9999,
                              label='Skilaboð')
    message.error_messages = {'required': 'Vinsamlega sláðu inn skilaboð'}
