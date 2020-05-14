from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductImage, Type, System, Manufacturer

def index(request):
    all_products = Product.objects.prefetch_related('system', 'type').all().order_by('name')

    if 'all' in request.GET:
        return JsonResponse({'data': [product.to_dict() for product in all_products]})
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            return JsonResponse({'data': [product.to_dict() for product in all_products.filter(name__icontains=search)]})

    search_results = __find_search_results(request, all_products)

    if search_results:
        return JsonResponse({'data': [product.to_dict() for product in search_results]})
    else:
        all_manufacturers = Manufacturer.objects.all()
        main_manufacturer_tuple = ('Nintendo', 'Sega', 'Sony', 'Microsoft')
        return render(request, 'product/products.html', {
            'types': Type.objects.all(),
            'systems': System.objects.prefetch_related('manufacturer').all(),
            'main_manufacturers': all_manufacturers.filter(name__in=main_manufacturer_tuple),
            'other_manufacturers': all_manufacturers.exclude(name__in=main_manufacturer_tuple),
            'products': all_products
        })

def __find_search_results(request, all_products):
    search_results = None
    if 'manufacturer' in request.GET:
        manufacturers = request.GET['manufacturer'].strip().split('_')
        if not search_results:
            search_results = all_products.filter(system__manufacturer__name__in=manufacturers)
        else:
            search_results |= all_products.filter(system__manufacturer__name__in=manufacturers)

    if 'system' in request.GET:
        systems = request.GET['system'].strip().split('_')
        if not search_results:
            search_results = all_products.filter(system__abbreviation__in=systems)
        else:
            search_results |= all_products.filter(system__abbreviation__in=systems)

    if 'type' in request.GET:
        types = request.GET['type'].strip().split('_')
        if not search_results:
            search_results = all_products.filter(type__name__in=types)
        else:
            search_results |= all_products.filter(type__name__in=types)

    return search_results

def get_product_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'product/product_detail.html', {
        'product': product,
        'images': images
    })

def get_product_json_by_id(request, id):
    try:
        product = Product.objects.prefetch_related('system', 'type').get(pk=id)
        return JsonResponse({
            'data': product.to_dict()
        })
    except Product.DoesNotExist:
        return JsonResponse({'data': {}})