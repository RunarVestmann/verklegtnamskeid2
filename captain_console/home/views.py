from django.shortcuts import render
from product.models import Product
from user.models import OrderProduct
from django.db.models import Count


# Create your views here.
def index(request):
    newest_products = Product.objects.prefetch_related('type', 'system').order_by('-shop_arrival_date')[:3]
    most_popular_product_ids = OrderProduct.objects.values('product').annotate(Count('product')).order_by('-product__count').values_list('product', flat=True)[:3]
    return render(request, 'home/index.html', {
        'newest_products': newest_products,
        'most_popular_products': Product.objects.filter(id__in=most_popular_product_ids)
    })
