from django.db import models
from product.models import Product

class ShoppingCart(models.Model):
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.products