from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ShippingForm, PaymentForm


def index(request):
    return render(request, 'cart/cart.html')


@login_required
def shipping_info(request):
    initial = {'si': request.session.get('si', None)}
    form = ShippingForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            ship_info = {}
            for field in form:
                ship_info[field.name] = form.cleaned_data[field.name]

            request.session['si'] = ship_info
            return redirect('payment')
    return render(request, 'cart/shipping.html', {'form': form})


@login_required
def payment_info(request):
    initial = {'ci': request.session.get('ci', None)}
    form = PaymentForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            card_info = {}
            for field in form:
                card_info[field.name] = form.cleaned_data[field.name]

            request.session['ci'] = card_info
            return redirect('overview')
    return render(request, 'cart/payment.html', {'form': form})


@login_required
def payment_overview(request):
    try:
        ci = request.session['ci']
        si = request.session['si']

        countries = ShippingForm.countries
        for c in countries:
            ''' gets humain frendly names back from code name'''
            if c[0] == si['country']:
                si['country_name'] = c[1]

    except:
        ci = 'ekkert hér'
        si = 'ekkert hér'

    return render(request, 'cart/overview.html', {'card_info': ci, 'ship_info': si})


@login_required
def receipt(request):
    return render(request, 'cart/receipt.html')
