from django.contrib import admin

# Register your models here.
from .models import Product, User
admin.site.register(User)
admin.site.register(Product)

