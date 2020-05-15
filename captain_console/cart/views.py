from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ShippingForm, PaymentForm
import json
from .models import ShoppingCart, ShoppingCartProducts
from product.models import Product
from user.models import Profile, Order, OrderProduct


def __user_has_no_cart_products(user_id):
    # Check whether the user has any products in his cart
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
    # The user goes back to the cart page if his cart is empty
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

    initial = {'shipping_info': request.session.get('shipping_info', None)}
    form = ShippingForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            ship_info = {}
            for field in form:
                ship_info[field.name] = form.cleaned_data[field.name]

            request.session['shipping_info'] = ship_info
            return redirect('payment')

    if initial['shipping_info']:
        shipping_info = initial['shipping_info']
        form.fields['name'].initial = shipping_info['name']
        form.fields['street_name'].initial = shipping_info['street_name']
        form.fields['house_nbr'].initial = shipping_info['house_nbr']
        form.fields['city'].initial = shipping_info['city']
        form.fields['zip_code'].initial = shipping_info['zip_code']
        form.fields['country'].initiall = shipping_info['country']
    return render(request, 'cart/shipping.html', {'form': form})


@login_required
def payment_info(request):
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

    initial = {'contact_info': request.session.get('contact_info', None)}

    if not request.session.get('shipping_info', None):
        return redirect('/cart/shipping')

    form = PaymentForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            card_info = {}
            for field in form:
                card_info[field.name] = form.cleaned_data[field.name]
            card_info['exp_day'] = card_info['exp_month'] + '/' + card_info['exp_year']
            request.session['contact_info'] = card_info
            return redirect('overview')

    if initial['contact_info']:
        contact_info = initial['contact_info']
        form.fields['name'].initial = contact_info['name']
        form.fields['card_nbr'].initial = contact_info['card_nbr']
        if 'exp_month' in initial:
            form.fields['exp_month'].initial = contact_info['exp_month']
        if 'exp_year' in initial:
            form.fields['exp_year'].initial = contact_info['exp_year']
        form.fields['cvc_nbr'].initial = contact_info['cvc_nbr']
    return render(request, 'cart/payment.html', {'form': form})


@login_required
def payment_overview(request):
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

    contact_info, shipping_info = get_session_info(request)

    if not shipping_info:
        return redirect('/cart/shipping')
    elif not contact_info:
        return redirect('/cart/payment')

    return render(request, 'cart/overview.html', {'card_info': contact_info, 'ship_info': shipping_info})


@login_required
def receipt(request):


    contact_info, shipping_info = get_session_info(request)

    if not shipping_info:
        return redirect('/cart/shipping')
    elif not contact_info:
        return redirect('/cart/payment')

    return render(request, 'cart/receipt.html', {'card_info': contact_info, 'ship_info': shipping_info})


def get_session_info(request):
    try:
        contact_info = request.session['contact_info']
    except:
        contact_info = False


    try:
        shipping_info = request.session['shipping_info']

        countries = ShippingForm.countries
        for c in countries:
            ''' gets human frendly names back from code name'''
            if c[0] == shipping_info['country']:
                shipping_info['country_name'] = c[1]

    except:
        shipping_info = False

    return contact_info, shipping_info


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
            profile.save()

        if not profile.shopping_cart:
            cart = ShoppingCart()
            cart.save()
            profile.shopping_cart = cart

        non_existing_product_id_list = []

        cart_products = ShoppingCartProducts.objects.filter(shopping_cart_id=profile.shopping_cart.id)
        if cart_products:
            cart_products.delete()

        if data:
            for product in data:
                try:
                    ShoppingCartProducts.objects.create(product=Product.objects.get(id=product['id']),
                                                        shopping_cart=profile.shopping_cart,
                                                        quantity=product['cartQuantity'])
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

@login_required
def order(request):
    if request.method == 'POST':
        contact_info, shipping_info = get_session_info(request)
        if not shipping_info:
            return JsonResponse({'data': {'redirect': '/cart/shipping'}, 'message': 'Vantar sendingarupplýsingar'})
        elif not contact_info:
            return JsonResponse({'data': {'redirect': '/cart/payment'}, 'message': 'Vantar Greiðsluupplýsingar '})

        # Getting the profile instance
        try:
            profile = Profile.objects.get(user__id=request.user.id)
        # Creating it if it doesn't exist
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()

        # Creating the order
        new_order = Order.objects.create(name=shipping_info['name'],
                          address=shipping_info['street_name'] + ' ' + shipping_info['house_nbr'],
                          city=shipping_info['city'],
                          zip=shipping_info['zip_code'],
                          country=shipping_info['country'],
                          profile=profile)

        # Setting the cart products into the join table
        cart_products = ShoppingCartProducts.objects.filter(shopping_cart_id=profile.shopping_cart.id)
        for cp in cart_products:
            OrderProduct.objects.create(quantity=cp.quantity,
                                        product=cp.product,
                                        order=new_order)

            # Reducing the product quantity and saving it
            cp.product.quantity -= cp.quantity
            cp.product.save()

        cart_products.delete()

        response = JsonResponse({'data': {'redirect': '/cart/receipt'}})
        response.status_code = 201
        return response
    else:
        response = JsonResponse({'data': {}, 'message': 'Unsupported method used, this route only supports POST'})
        response.status_code = 400
        return response
