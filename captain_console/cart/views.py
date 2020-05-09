from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def index(request):
    return render(request, 'cart/cart.html')

@login_required
def shipping_info(request):
    return render(request, 'cart/shipping.html')

@login_required
def payment_info(request):
    return render(request, 'cart/payment.html')

@login_required
def payment_overview(request):
    return render(request, 'cart/overview.html')

@login_required
def receipt(request):
    return render(request, 'cart/receipt')