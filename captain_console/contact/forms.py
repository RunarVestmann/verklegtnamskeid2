from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=100)
    name.label = 'Nafn'
    name.error_messages = {'required': 'Vinsamlega sláðu inn nafn'}
    from_email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=True, max_length=100)
    from_email.label = 'Netfang'
    from_email.error_messages = {'required': 'Vinsamlega sláðu inn netfang'}
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=True, max_length=9999)
    message.label = 'Skilaboð'
    message.error_messages = {'required': 'Vinsamlega sláðu inn skilaboð'}
