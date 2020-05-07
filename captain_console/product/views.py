from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, ProductImage, Type, System

def index(request):
    # Store at the top what we'll be using no matter what
    all_types = Type.objects.all()
    all_products = Product.objects.prefetch_related('system', 'type').all()

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
            count = 0
            for t in all_types:
                if t.name in search:
                    count += 1

            # Only filter out unwanted types if there are 1 to n-1 filters active
            if not (count == 0 or count == len(all_types)):
                for t in all_types:
                    if t.name not in search:
                        search_results = search_results.exclude(type__name=t.name)

        else:
            search_results = all_products

        # Make a list of dictionaries that contain each products data
        products = [{
            'id': p.id,
            'name': p.name,
            'quantity': p.quantity,
            'description': p.description,
            'price': p.price,
            'system': {
                'manufacturer': p.system.manufacturer.name,
                'abbreviation': p.system.abbreviation,
                'name': p.system.name
            },
            'release_date': p.release_date,
            'shop_arrival_date': p.shop_arrival_date,
            'type': p.type.name,
            'first_image': p.productimage_set.first().image.url
        } for p in search_results]

        return JsonResponse({'data': products})

    # If the user did not enter a search string we simply return all products in an html
    return render(request, 'product/products.html', {
        'products': all_products,
        'types': all_types,
        'systems': System.objects.prefetch_related('manufacturer').all()
    })

def __get_search_results(query_set, word):
    return query_set.filter(name__icontains=word) \
         | query_set.filter(system__name__icontains=word) \
         | query_set.filter(system__manufacturer__name__icontains=word) \
         | query_set.filter(system__abbreviation__icontains=word)

def get_product_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    images = ProductImage.objects.filter(product=product)
    return render(request, 'product/product_detail.html', {
        'product': product,
        'images': images
    })

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