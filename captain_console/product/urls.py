from django.urls import path
from . import views

urlpatterns = [
    # http://localhost:8000/products
    path('', views.index, name='products'),
    path('<int:id>', views.get_product_by_id, name='product_details')
]