# Create your models here.
from django.db.models import Model, CharField, ForeignKey, CASCADE
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Social(Model):
    name = CharField(max_length=20, default=None, null=False)
    icon = CharField(max_length=100, default=None, null=True)
    button_css_class = CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class SocialUser(Model):
    social = ForeignKey(Social, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    url = CharField(max_length=500, default=None, null=False)

    def __str__(self):
        return "{}_{}".format(self.social.__str__(), self.user.__str__())
