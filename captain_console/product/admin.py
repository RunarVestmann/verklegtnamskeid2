from django.contrib import admin
from .models import Product, ProductImage, Manufacturer, System, Type

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

    class Meta:
        model = Product

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Manufacturer)
admin.site.register(System)
admin.site.register(Type)