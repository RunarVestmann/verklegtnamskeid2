from django.db import models
from product.models import Product

class ShoppingCart(models.Model):
    products = models.ManyToManyField(Product, through='ShoppingCartProducts')

class ShoppingCartProducts(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()