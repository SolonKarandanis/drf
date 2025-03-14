import pgtrigger
from django.db.models import QuerySet, DateTimeField, EmailField, UUIDField, \
    TextField, BooleanField, Model, OneToOneField, CASCADE, CharField, TextChoices, FileField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Lower
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from datetime import date
import uuid
import pghistory


class UserStatus(TextChoices):
    UNVERIFIED = 'user.unverified',
    ACTIVE = 'user.active',
    DEACTIVATED = 'user.deactivated',
    DELETED = 'user.deleted'


class UserQuerySet(QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

    def is_verified(self):
        return self.filter(is_verified=True)

    def is_staff(self):
        return self.filter(is_staff=True)

    def with_groups(self):
        return self.prefetch_related('groups')

    def with_details(self):
        return self.select_related('user_details')


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def update_user(self, user):
        user = user.save()
        return user

    def get_queryset(self, *args, **kwargs):
        return UserQuerySet(self.model, using=self._db)

    def create_user(self, email, password, **extra_fields):
        """
       Create and save a user with the given email and password.
       """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", False)
        extra_fields.setdefault("status", UserStatus.UNVERIFIED)
        if not email:
            raise ValueError(_("user.email.required"))
        if extra_fields.get("is_staff") is not False:
            raise ValueError(_("user.is_staff.false"))
        if extra_fields.get("is_superuser") is not False:
            raise ValueError(_("user.is_superuser.false"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.uuid = uuid.uuid4()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("status", UserStatus.ACTIVE)
        extra_fields.setdefault("uuid", uuid.uuid4())

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("superuser.is_staff.true"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("superuser.is_superuser.true"))
        return self.create_user(email, password, **extra_fields)

    def revert_change(self, version_id: int):
        """Rewind to a previous version"""
        try:
            return self.events.get(id=version_id).revert()
        except IndexError:
            return self

    def revert_to_previous_change(self):
        """Rewind to the previous version"""
        try:
            return self.events.order_by("-pgh_id")[1].revert()
        except IndexError:
            return self


# Create your models here.
@pghistory.track(append_only=True)
class User(AbstractUser):
    created_date = DateTimeField(auto_now_add=True, null=False)
    updated_date = DateTimeField(auto_now=True, null=False)
    email = EmailField(_("email.address"), unique=True)
    uuid = UUIDField(default=uuid.uuid4())
    images = GenericRelation("images.Images", related_query_name='user')
    bio = TextField(default=None, null=True)
    is_verified = BooleanField(db_default=False)
    status = CharField(max_length=40, choices=UserStatus.choices, db_default=UserStatus.UNVERIFIED)
    cv = FileField(upload_to='cvs/', null=True, blank=True)
    uploaded_at = DateTimeField(null=True, blank=True)

    date_joined = None

    class Meta:
        ordering = [Lower('username')]
        triggers = [
            pgtrigger.SoftDelete(
                name="pgtrigger_softdelete_is_active",
                field="is_active",
                value=False,
            ),
            pgtrigger.SoftDelete(
                name="pgtrigger_softdelete_status",
                field="status",
                value=UserStatus.DELETED,
            )
        ]

    objects = UserManager()

    def __str__(self):
        return f"<User username:{self.username} uuid:{self.uuid}>"

    def __repr__(self):
        return f"<User username:{self.username} uuid:{self.uuid}>"

    @property
    def was_created_this_year(self) -> bool:
        current_year = timezone.now().year
        return self.created_date.date().year == current_year

    def was_created_after(self, given_date: date) -> bool:
        return self.created_date.date() > given_date


class UserDetailsManager(BaseUserManager):

    def update_details(self, details):
        details = details.save()
        return details


class UserDetails(Model):
    user = OneToOneField(User, on_delete=CASCADE, primary_key=True, related_name='user_details')
    country = CharField(max_length=120, default=None, null=True)
    state = CharField(max_length=120, default=None, null=True)
    city = CharField(max_length=120, default=None, null=True)
    address = CharField(max_length=120, default=None, null=True)
    zip = CharField(max_length=20, default=None, null=True)
    phone = CharField(max_length=50, default=None, null=True)

    objects = UserDetailsManager()

    def __str__(self):
        return f"{self.state}-{self.city}-{self.address}"
