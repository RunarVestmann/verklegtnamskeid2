from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'cart/cart.html')

def shipping_info(request):
    return render(request, 'cart/shipping.html')

def payment_info(request):
    return render(request, 'cart/payment.html')

def payment_overview(request):
    return render(request, 'cart/overview.html')

def receipt(request):
    return render(request, 'cart/receipt')