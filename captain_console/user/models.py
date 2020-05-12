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

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if self.image.url != '' and this.image != self.image and this.image.url != '/media/images/profile/default_profile_image.svg':
                this.image.delete(save=False)
        except:
            pass
        super(Profile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            self.image.delete(save=False)
        except:
            pass
        super(Profile, self).delete(*args, **kwargs)

class Search(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_of_search = models.DateTimeField(default=timezone.now)

class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product)
    order_date = models.DateTimeField(default=timezone.now)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)