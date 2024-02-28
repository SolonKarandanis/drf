from django.db.models import QuerySet, DateTimeField, EmailField, UUIDField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.contrib.contenttypes.fields import GenericRelation
import uuid


class UserQuerySet(QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

    def is_staff(self):
        return self.filter(is_staff=True)

    def with_groups(self):
        return self.prefetch_related('groups')


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def get_queryset(self, *args, **kwargs):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, email, password, **extra_fields):
        """
       Create and save a user with the given email and password.
       """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        if not email:
            raise ValueError(_("user.email.required"))
        if extra_fields.get("is_staff") is not False:
            raise ValueError(_("user.is_staff.false"))
        if extra_fields.get("is_superuser") is not False:
            raise ValueError(_("user.is_superuser.false"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser.is_staff.true"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser.is_superuser.true"))
        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    created_date = DateTimeField(auto_now_add=True, null=False)
    updated_date = DateTimeField(auto_now=True, null=False)
    email = EmailField(_("email.address"), unique=True)
    uuid = UUIDField(default=uuid.uuid4())
    images = GenericRelation("images.Images", related_query_name='user')

    date_joined = None

    class Meta:
        ordering = [Lower('username')]

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
