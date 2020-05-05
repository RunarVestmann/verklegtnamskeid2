from django.db import models
from datetime import date

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class System(models.Model):
    abbreviation = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    system = models.ForeignKey(System, on_delete=models.DO_NOTHING)
    release_date = models.DateField()
    shop_arrival_date = models.DateField(default=date.today, blank=True)
    type = models.ForeignKey(Type, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.image.url