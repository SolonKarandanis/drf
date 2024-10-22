from django.contrib import admin

# Register your models here.
from .models import Product, Brand, Category, Attribute, AttributeOptions, ProductAttributeValues

admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(AttributeOptions)
admin.site.register(ProductAttributeValues)
