from django.contrib import admin

# Register your models here.
from .models import User, UserDetails

admin.site.register(User)
admin.site.register(UserDetails)
