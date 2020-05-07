from django.shortcuts import render
from product.models import Product

# Create your views here.
def index(request):
    return render(request, 'home/index.html', {
        'products': Product.objects.prefetch_related('system', 'type').all().order_by('-shop_arrival_date')
    })