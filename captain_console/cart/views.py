from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ShippingForm, PaymentForm
import json
from .models import ShoppingCart, ShoppingCartProducts
from product.models import Product
from user.models import Profile

def __user_has_no_cart_products(user_id):
    try:
        cart = Profile.objects.get(user_id=user_id).shopping_cart
        if not cart or not cart.products.all():
            return True
    except Product.DoesNotExist:
        return True
    return False

def index(request):
    return render(request, 'cart/cart.html')

@login_required
def shipping_info(request):
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

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
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

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
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

    try:
        ci = request.session['ci']
        si = request.session['si']

        countries = ShippingForm.countries
        for c in countries:
            ''' gets human frendly names back from code name'''
            if c[0] == si['country']:
                si['country_name'] = c[1]
    except:
        ci = 'ekkert hér'
        si = 'ekkert hér'
    return render(request, 'cart/overview.html', {'card_info': ci, 'ship_info': si})

@login_required
def receipt(request):
    return render(request, 'cart/receipt.html')

@login_required
def sync_cart(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            response = JsonResponse({'data': {}, 'message': 'Invalid JSON format'})
            response.status_code = 400
            return response
        try:
            profile = Profile.objects.get(user__id=request.user.id)

        # Create a profile if the user doesn't seem to have one
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)

        if not profile.shopping_cart:
            cart = ShoppingCart()
            cart.save(False)
            profile.shopping_cart = cart

        non_existing_product_id_list = []

        if not data:
            cart_products = ShoppingCartProducts.objects.filter(shopping_cart_id=profile.shopping_cart.id)
            if cart_products:
                cart_products.delete()
        else:
            for product in data:
                try:
                    ShoppingCartProducts.objects.create(product=Product.objects.get(id=product['id']),
                                                        shopping_cart=profile.shopping_cart, quantity=product['cartQuantity'])
                except Product.DoesNotExist:
                    non_existing_product_id_list.append(product['id'])

        profile.save()

        if non_existing_product_id_list:
            return JsonResponse({'data': data, 'nonExistingProductIds': non_existing_product_id_list})
        else:
            return JsonResponse({'data': data})

    else:
        response = JsonResponse({'data': {}, 'message': 'Unsupported method used'})
        response.status_code = 405
        return response