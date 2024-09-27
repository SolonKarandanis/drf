import logging
from typing import List

from auth.models import User
from billing.models import Card

logger = logging.getLogger('django')


class CardRepository:

    def find_user_cards(self, user_id: int) -> List[Card]:
        return Card.objects.filter(user_id=user_id)

    def create_user_card(self, logged_in_user: User, card: Card) -> None:
        pass

