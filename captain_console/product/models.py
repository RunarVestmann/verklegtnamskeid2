from django.db import models
from datetime import date

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.CharField(max_length=999)
    price = models.IntegerField()
    manufacturer = models.OneToOneField(Manufacturer, on_delete=models.DO_NOTHING)
    release_date = models.DateField()
    shop_arrival_date = models.DateField(default=date.today, blank=True)

class ProductImage(models.Model):
    image: models.CharField(max_length=999)
    product: models.ForeignKey(Product, on_delete=models.CASCADE)