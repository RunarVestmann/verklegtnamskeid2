from django.contrib.auth.models import User
from django.db import models
from product.models import Product
#from cart.models import ShoppingCart
from datetime import datetime

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    #shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete(save=False)
        except:
            pass
        super(Profile, self).save(*args, **kwargs)

class Search(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_of_search = models.DateTimeField(default=datetime.now)