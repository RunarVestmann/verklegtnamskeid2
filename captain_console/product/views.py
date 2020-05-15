from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Product, ProductImage, Type, System, Manufacturer

# The landing page for /products
def index(request):
    product_objects = Product.objects.prefetch_related('system', 'type').order_by('name')

    if 'noproducts' in request.GET and request.path != '/products?noproducts':
        main_manufacturer_tuple = ('Nintendo', 'Sega', 'Sony', 'Microsoft')
        return render(request, 'product/products.html', {
            'types': Type.objects.all(),
            'systems': System.objects.prefetch_related('manufacturer').all(),
            'main_manufacturers': Manufacturer.objects.filter(name__in=main_manufacturer_tuple),
            'other_manufacturers': Manufacturer.objects.exclude(name__in=main_manufacturer_tuple),
            'products': []
        })

    if 'all' in request.GET:
        return JsonResponse({'data': __get_list_of_dicts(product_objects.all())})
    if 'search' in request.GET:
        search = request.GET['search']
        if search:
            return JsonResponse({'data': __get_list_of_dicts(product_objects.filter(name__icontains=search)
                                                            |product_objects.filter(system__manufacturer__name__icontains=search)
                                                            |product_objects.filter(system__name__icontains=search)
                                                            |product_objects.filter(system__abbreviation__icontains=search))})

    search_results, found_results = __find_search_results(request, product_objects)

    if found_results:
        return JsonResponse({'data': __get_list_of_dicts(search_results)})
    else:
        main_manufacturer_tuple = ('Nintendo', 'Sega', 'Sony', 'Microsoft')
        return render(request, 'product/products.html', {
            'types': Type.objects.all(),
            'systems': System.objects.prefetch_related('manufacturer').all(),
            'main_manufacturers': Manufacturer.objects.filter(name__in=main_manufacturer_tuple),
            'other_manufacturers': Manufacturer.objects.exclude(name__in=main_manufacturer_tuple),
            'products': __get_list_of_dicts(product_objects.all())
        })

def __get_list_of_dicts(query_set):
    return [product.to_dict(ProductImage.objects.filter(product_id=product.id).first()) for product in query_set]

def __find_search_results(request, product_objects):
    search_results = None
    found_results = False
    if 'manufacturer' in request.GET:
        found_results = True
        manufacturers = request.GET['manufacturer'].strip().split('_')
        search_results = product_objects.filter(system__manufacturer__name__in=manufacturers)

    if 'system' in request.GET:
        found_results = True
        systems = request.GET['system'].strip().split('_')
        if not search_results:
            search_results = product_objects.filter(system__abbreviation__in=systems)
        else:
            search_results = search_results.filter(system__abbreviation__in=systems)

    if 'type' in request.GET:
        found_results = True
        types = request.GET['type'].strip().split('_')
        if not search_results:
            search_results = product_objects.filter(type__name__in=types)
        else:
            search_results = search_results.filter(type__name__in=types)

    return search_results, found_results

# A more detailed view for a given product
def get_product_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'product/product_detail.html', {
        'product': product,
        'images': images
    })

# A view that returns a given product as json
def get_product_json_by_id(request, id):
    try:
        product = Product.objects.prefetch_related('system', 'type').get(pk=id)
        return JsonResponse({
            'data': product.to_dict()
        })
    except Product.DoesNotExist:
        return JsonResponse({'data': {}})