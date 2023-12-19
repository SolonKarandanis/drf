from django.contrib import admin
from .models import Comment


# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'content', 'object_id', 'content_type', 'content_object'
    ]


admin.site.register(Comment, CommentAdmin)
