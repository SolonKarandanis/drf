from django.contrib import admin

# Register your models here.
from .models import Social, SocialUser

admin.site.register(Social)
admin.site.register(SocialUser)
