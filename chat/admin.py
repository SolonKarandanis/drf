from django.contrib import admin

# Register your models here.
from .models import Room, Message, Event

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Event)
