from django.shortcuts import render, get_object_or_404
from .models import Product

def index(request):
    return render(request, 'product/products.html')

def get_product_by_id(request, id):
    return render(request, 'product/product_detail.html', {
        'product': get_object_or_404(Product, pk=id)
    })