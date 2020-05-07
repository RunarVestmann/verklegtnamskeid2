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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'description': self.description,
            'price': self.price,
            'system': {
                'name': self.system.name,
                'abbreviation': self.system.abbreviation,
                'manufacturer': self.system.manufacturer.name
            },
            'release_date': self.release_date,
            'shop_arrival_date': self.shop_arrival_date,
            'type': self.type.name,
            'first_image': self.productimage_set.first().image.url
        }

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def save(self, *args, **kwargs):
        try:
            this = ProductImage.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except ProductImage.DoesNotExist:
            pass
        super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url