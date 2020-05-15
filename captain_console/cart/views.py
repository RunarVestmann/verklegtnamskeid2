from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import ShippingForm, PaymentForm
import json
from .models import ShoppingCart, ShoppingCartProducts
from product.models import Product
from user.models import Profile, Order, OrderProduct


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

    if initial['si']:
        si = initial['si']
        form.fields['name'].initial = si['name']
        form.fields['street_name'].initial = si['street_name']
        form.fields['house_nbr'].initial = si['house_nbr']
        form.fields['city'].initial = si['city']
        form.fields['zip_code'].initial = si['zip_code']
        form.fields['country'].initiall = si['country']
    return render(request, 'cart/shipping.html', {'form': form})


@login_required
def payment_info(request):
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')

    initial = {'ci': request.session.get('ci', None)}

    if not request.session.get('si', None):
        return redirect('/cart/shipping')

    form = PaymentForm(request.POST or None, initial=initial)
    if request.method == 'POST':
        if form.is_valid():
            card_info = {}
            for field in form:
                card_info[field.name] = form.cleaned_data[field.name]
            card_info['exp_day'] = card_info['exp_month'] + '/' + card_info['exp_year']
            request.session['ci'] = card_info
            return redirect('overview')

    if initial['ci']:
        ci = initial['ci']
        form.fields['name'].initial = ci['name']
        form.fields['card_nbr'].initial = ci['card_nbr']
        form.fields['exp_month'].initial = ci['exp_month']
        form.fields['exp_year'].initial = ci['exp_year']
        form.fields['cvc_nbr'].initial = ci['cvc_nbr']
    return render(request, 'cart/payment.html', {'form': form})


@login_required
def payment_overview(request):
    if __user_has_no_cart_products(request.user.id):
        return redirect('/cart')


    ci, si = get_session_info(request)

    if not si:
        return redirect('/cart/shipping')
    elif not ci:
        return redirect('/cart/payment')


    return render(request, 'cart/overview.html', {'card_info': ci, 'ship_info': si})


@login_required
def receipt(request):


    ci, si = get_session_info(request)

    if not si:
        return redirect('/cart/shipping')
    elif not ci:
        return redirect('/cart/payment')

    return render(request, 'cart/receipt.html', {'card_info': ci, 'ship_info': si})


def get_session_info(request):
    try:
        ci = request.session['ci']
    except:
        ci = False


    try:
        si = request.session['si']

        countries = ShippingForm.countries
        for c in countries:
            ''' gets human frendly names back from code name'''
            if c[0] == si['country']:
                si['country_name'] = c[1]

    except:
        si = False

    return ci, si


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
        ci, si = get_session_info(request)
        if not si:
            return JsonResponse({'data': {'redirect': '/cart/shipping'}, 'message': 'Vantar sendingarupplýsingar'})
        elif not ci:
            return JsonResponse({'data': {'redirect': '/cart/payment'}, 'message': 'Vantar Greiðsluupplýsingar '})

        # Getting the profile instance
        try:
            profile = Profile.objects.get(user__id=request.user.id)
        # Creating it if it doesn't exist
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()

        # Creating the order
        new_order = Order.objects.create(name=si['name'],
                          address=si['street_name'] + ' ' + si['house_nbr'],
                          city=si['city'],
                          zip=si['zip_code'],
                          country=si['country'],
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
