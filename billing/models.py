import datetime

from django.db.models import Model, ForeignKey, SET_NULL, TextChoices, CharField, DateTimeField, BooleanField, CASCADE, \
    IntegerField
from django.conf import settings

User = settings.AUTH_USER_MODEL


class CardType(TextChoices):
    VISA = 'card.type.visa',
    MASTERCARD = 'card.type.mastercard',


class CardStatus(TextChoices):
    ACTIVE = 'card.active',
    DEACTIVATED = 'card.deactivated',
    DELETED = 'card.deleted'
    EXPIRED = 'card.expired',


# Create your models here.
class Card(Model):
    current_year = datetime.date.today().year
    YEAR_CHOICES = [(y, y) for y in range(current_year, current_year + 5)]
    MONTH_CHOICE = [(m, m) for m in range(1, 12)]

    number = CharField(max_length=20, null=False)
    type = CharField(max_length=40, choices=CardType.choices)
    status = CharField(max_length=40, choices=CardStatus.choices, default=CardStatus.ACTIVE)
    expiration_month = IntegerField(choices=MONTH_CHOICE, null=False)
    expiration_year = IntegerField(choices=YEAR_CHOICES, null=False)
    cpv = CharField(max_length=3, null=False)
    is_active = BooleanField(db_default=True)
    is_selected = BooleanField(db_default=False)
    date_created = DateTimeField(auto_now_add=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE, default=1)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.number}"

    def __repr__(self):
        return f"<Card {self.number}>"

    @property
    def expiry_date(self) -> str:
        return "{}/{}".format(self.expiration_month.__str__(), self.expiration_year.__str__())

    @property
    def is_expired(self) -> bool:
        current_date = datetime.date.today()
        current_month = current_date.month
        current_year = current_date.year

        if self.expiration_year < current_year:
            return True
        if self.expiration_year == current_year and self.expiration_month < current_month:
            return True
        return False

