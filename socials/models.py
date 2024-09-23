# Create your models here.
from django.db.models import Model, CharField, ForeignKey, CASCADE, Manager, ManyToManyField
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Social(Model):
    name = CharField(max_length=20, default=None, null=False)
    icon = CharField(max_length=100, default=None, null=True)
    button_css_class = CharField(max_length=100, null=True)
    users = ManyToManyField(User, through="SocialUser")

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"<Social {self.name}>"


class SocialUserManager(Manager):

    def initialize_social_user(self, social_id: int, user_id: int, url: str):
        social_user = self.create(social_id=social_id, user_id=user_id, url=url)
        return social_user


class SocialUser(Model):
    social = ForeignKey(Social, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    url = CharField(max_length=500, default=None, null=False)

    objects = SocialUserManager()

    def __str__(self):
        return "{}_{}".format(self.social.__str__(), self.user.__str__())
