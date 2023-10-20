from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def __str__(self):
        return f"{self.username}"
