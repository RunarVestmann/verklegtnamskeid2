from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product, ProductImage

def index(request):
    return render(request, 'product/products.html')

def get_product_by_id(request, id):
    return render(request, 'product/product_detail.html', {
        'product': get_object_or_404(Product, pk=id)
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