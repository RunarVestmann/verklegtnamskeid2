from django.http import JsonResponse
from django.shortcuts import render
from user.models import Profile
from product.models import Product
import json

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

def user_cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.prefetch_related('shopping_cart__products').get(user=request.user)
                return JsonResponse({'data': profile.shopping_cart})
            except Profile.DoesNotExist:
                response = JsonResponse({'data': {}, 'message': 'User profile was not found'})
                response.status_code = 404
                return response
        else:
            response = JsonResponse({'data': {}, 'message': 'Log in required to get cart details'})
            response.status_code = 401
            return response

    elif request.method == 'PUT':
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.prefetch_related('shopping_cart__products').get(user=request.user)
            except Profile.DoesNotExist:
                response = JsonResponse({'data': {}, 'message': 'User profile was not found'})
                response.status_code = 404
                return response
            try:
                cart = json.loads(request.body)
                # TODO: Somehow delete the old carts values and add these ones...

            except json.JSONDecodeError:
                return JsonResponse({'data': {}, 'message': 'The body did not contain valid JSON'})

    else:
        response = JsonResponse({'data': {}, 'message': 'This route only supports GET and PUT'})
        response.status_code = 400
        return response
