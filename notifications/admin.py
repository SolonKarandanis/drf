from django.contrib import admin

from .models import BroadcastNotification, NotificationEvent

admin.site.register(BroadcastNotification)
admin.site.register(NotificationEvent)