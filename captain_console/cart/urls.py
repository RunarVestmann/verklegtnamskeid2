from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/cart
    path('', views.index, name="cart"),

    # http://localhost:8000/cart/shipping
    path('shipping', views.shipping_info, name='shipping'),

    # http://localhost:8000/cart/payment
    path('payment', views.payment_info, name='payment'),

    # http://localhost:8000/cart/overview
    path('overview', views.payment_overview, name='overview'),

    # http://localhost:8000/cart/receipt
    path('receipt', views.receipt, name='receipt'),

    # http://localhost:8000/cart/sync => PUT request
    path('sync', views.sync_cart, name='sync_cart'),

    # http://localhost:8000/cart/order
    path('order', views.order, name='order'),
]