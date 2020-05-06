from django.db.models import QuerySet
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, ProductImage, Type, System

def index(request):
    if 'search' in request.GET:
        search = request.GET['search'].strip().split()

        if search:
            search_results = Product.objects.filter(name__icontains=search[0]) \
                           | Product.objects.filter(system__name__icontains=search[0]) \
                           | Product.objects.filter(system__manufacturer__name__icontains=search[0]) \
                           | Product.objects.filter(system__abbreviation__icontains=search[0]) \
                           | Product.objects.filter(type__name__icontains=search[0])

            for word in search[1:]:
                search_results = search_results \
                               | Product.objects.filter(name__icontains=word) \
                               | Product.objects.filter(system__name__icontains=word) \
                               | Product.objects.filter(system__manufacturer__name__icontains=word) \
                               | Product.objects.filter(system__abbreviation__icontains=word) \
                               | Product.objects.filter(type__name__icontains=word)

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

        else:
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
            } for p in Product.objects.all()]

            return JsonResponse({'data': products})

    return render(request, 'product/products.html', {
        'products': Product.objects.all(),
        'types': Type.objects.all(),
        'systems': System.objects.all()
    })

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