from django.contrib.auth.models import User
from django.db import models
from cart.models import ShoppingCart
from product.models import Product
from django.utils import timezone
import pytz

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profile/', default='images/profile/default_profile_image.svg')
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE, null=True)

    # Save method that makes sure that we don't delete the default img if we're replacing it
    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if self.image != this.image and this.image.url != '/media/images/profile/default_profile_image.svg':
                this.image.delete(save=False)
        except:
            pass
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Search(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_of_search = models.DateTimeField(default=timezone.now)

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through='OrderProduct')
    order_date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f'Pöntun nr.{self.id} fyrir {self.name}'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Vara fyrir pöntun nr.{self.order.id}'
