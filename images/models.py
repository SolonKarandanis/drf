from django.db.models import Model, CharField, TextField, ForeignKey, PositiveSmallIntegerField, DateTimeField, CASCADE, \
    ImageField, BooleanField, UniqueConstraint, Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

User = settings.AUTH_USER_MODEL


def user_directory_path(instance, filename):
    return 'images/'


# Create your models here.
class Images(Model):
    title = CharField(max_length=250)
    alt = TextField(null=True)
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = DateTimeField(auto_now_add=True, null=False)
    image = ImageField(
        upload_to='images/', default='posts/default.jpg')
    uploaded_by = ForeignKey(User, on_delete=CASCADE)
    uploaded_at = DateTimeField(auto_now=True, null=True)
    is_profile_image = BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                name='one_user_profile_image',
                fields=['object_id', 'is_profile_image', 'content_type'],
                condition=Q(is_profile_image=True) & Q(content_type=17)
            )
        ]

    def __repr__(self):
        return f"<Images id:{self.id} , title: {self.title}>"
