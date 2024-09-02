from django.db.models import Model, CharField, TextField, ForeignKey, PositiveSmallIntegerField, DateTimeField, CASCADE, \
    ImageField, BooleanField, UniqueConstraint, Q, IntegerField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

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
    size = IntegerField(blank=True, null=True)
    image_type = CharField(max_length=20, null=True)

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


# delete previous profile image before saving new one
@receiver(pre_save, sender=Images, dispatch_uid='profile_image_deleted')
def profile_image_deleted_handler(sender, instance, **kwargs):
    if instance.id is not None and instance.is_profile_image:
        for field in instance._meta.fields:
            if field.name == "icon":
                file = getattr(instance, field.name)
                if file:
                    file.delete(save=False)


# delete file from server
@receiver(pre_delete, sender=Images, dispatch_uid='image_deleted')
def image_deleted_handler(sender, instance, **kwargs):
    file = getattr(instance, "image")
    file.delete(save=False)
