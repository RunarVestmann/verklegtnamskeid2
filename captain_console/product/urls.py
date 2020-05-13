from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/products
    path('', views.index, name='products'),

    # http://localhost:8000/products/{id}
    path('<int:id>', views.get_product_by_id, name='product_details'),

    # http://localhost:8000/products/{id}/json
    path('<int:id>/json', views.get_product_json_by_id, name='product_json'),

    # http://localhost:8000/products/json
    path('json', views.get_products_json, name='products_json'),
]
