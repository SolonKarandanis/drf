from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

    def is_staff(self):
        return self.filter(is_staff=True)


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
            raise ValueError(_("The Email must be set"))
        if extra_fields.get("is_staff") is not False:
            raise ValueError(_("User cannot have is_staff=True."))
        if extra_fields.get("is_superuser") is not False:
            raise ValueError(_("User cannot have is_superuser=True."))
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
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class UserType(models.Model):
    CUSTOMER = 1
    SELLER = 2
    TYPE_CHOICES = (
        (SELLER, 'Seller'),
        (CUSTOMER, 'Customer')
    )

    id = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


# Create your models here.
class User(AbstractUser):
    user_type = models.ManyToManyField(UserType)
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    updated_date = models.DateTimeField(auto_now=True, null=False)
    email = models.EmailField(_("email address"), unique=True)

    class Meta:
        ordering = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.username}"
