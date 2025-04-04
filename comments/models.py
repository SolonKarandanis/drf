from django.db.models import Model, DateTimeField, TextField, ForeignKey, CASCADE, \
    PositiveSmallIntegerField, QuerySet, Manager, CharField, EmailField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CommentQuerySet(QuerySet):

    def get_order_not_shipped_comments(self):
        return self.filter(order__order_is_shipped=False)


class CommentManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return CommentQuerySet(self.model, using=self._db)


# Create your models here.
class Comment(Model):
    content = TextField()
    content_type = ForeignKey(ContentType, on_delete=CASCADE)  #products.product
    object_id = PositiveSmallIntegerField()                    #product.id
    content_object = GenericForeignKey('content_type', 'object_id')
    date_created = DateTimeField(auto_now_add=True, null=False)
    user = ForeignKey(User,  on_delete=CASCADE)
    user_username = CharField(max_length=50, null=True)
    user_email = EmailField(null=True)
    user_first_name = CharField(max_length=50, null=True)
    user_last_name = CharField(max_length=50, null=True)

    objects = CommentManager()

    def __repr__(self):
        return f"<Comment id:{self.id} , content: {self.content}>"
