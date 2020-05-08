from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm


# Create your views here.
def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail('Skilaboð frá: ' + name + '. Svarist til: ' + from_email, message, from_email, ['captainconsolestaff@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect('success')
    return render(request, "contact/contact.html", {'form': form})

def successView(request):
    return render(request, 'contact/success.html')