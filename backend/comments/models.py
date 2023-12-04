from django.db.models import Model, DateTimeField, TextField, ForeignKey, CASCADE, PositiveSmallIntegerField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

User = settings.AUTH_USER_MODEL


# Create your models here.
class Comment(Model):
    content = TextField()
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = DateTimeField(auto_now_add=True, null=False)
