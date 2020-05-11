from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import ShippingForm

def index(request):
    return render(request, 'cart/cart.html')

@login_required
def shipping_info(request):
    if request.method == 'GET':
        form = ShippingForm
    else:
        form = ShippingForm(request.POST)
        if form.is_valid():
            print('do somthing')

    return render(request, 'cart/shipping.html', {'form': form})

@login_required
def payment_info(request):
    return render(request, 'cart/payment.html')

@login_required
def payment_overview(request):
    return render(request, 'cart/overview.html')

@login_required
def receipt(request):
    return render(request, 'cart/receipt.html')