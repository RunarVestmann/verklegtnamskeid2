from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, ProductImage, Type, System, Manufacturer

def index(request):
    # Store at the top what we'll be using no matter what
    all_types = Type.objects.all()
    all_products = Product.objects.prefetch_related('system', 'type').all()
    all_manufacturers = Manufacturer.objects.all()

    # If the user entered a search string we find the results
    if 'search' in request.GET:
        search = request.GET['search'].strip().split()

        search_results = None
        if search:
            query_set = all_products

            # For every word in the search string get results from searching for that word
            search_results = __get_search_results(query_set, search[0])
            for i in range(1, len(search)):
                search_results |= __get_search_results(query_set, search[i])

            # Count how many filter types are active
            type_count = 0
            for t in all_types:
                if t.name in search:
                    type_count += 1

            # Only filter out unwanted types if there are 1 to n-1 filters active
            if not (type_count == 0 or type_count == len(all_types)):
                for t in all_types:
                    if t.name not in search:
                        search_results = search_results.exclude(type__name=t.name)

            # Count how many filter types are active
            man_count = 0
            for manufacturer in all_manufacturers:
                if manufacturer.name in search:
                    man_count += 1

            # Only filter out unwanted types if there are 1 to n-1 filters active
            if not (man_count == 0 or man_count == len(all_manufacturers)):
                for manufacturer in all_manufacturers:
                    if manufacturer.name not in search:
                        search_results = search_results.exclude(system__manufacturer__name=manufacturer.name)

        else:
            search_results = all_products

        # Make a list of dictionaries that contain each products data
        products = [product.to_dict() for product in search_results]

        return JsonResponse({'data': products})

    # If the user did not enter a search string we simply return all products in an html
    return render(request, 'product/products.html', {
        'products': all_products,
        'types': all_types,
        'systems': System.objects.prefetch_related('manufacturer').all(),
        'manufacturers': all_manufacturers
    })

def __get_search_results(query_set, word):
    return query_set.filter(name__icontains=word) \
         | query_set.filter(system__name__icontains=word) \
         | query_set.filter(system__manufacturer__name__icontains=word) \
         | query_set.filter(system__abbreviation__icontains=word) \
         | query_set.filter(type__name__icontains=word)

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

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(data=request.POST)
        if form.is_valid():
            product = form.save()
            image = ProductImage(image=request.POST['image'].path, product=product)
            image.save()
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'product/create_product.html', {
        'form': form
    })