from django.db import models
from product.models import Product

# Create your models here.
class ShoppingCart(models.Model):
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.products