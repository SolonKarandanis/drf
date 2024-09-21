import logging
from typing import List

from auth.models import User
from billing.models import Card

logger = logging.getLogger('django')


class CardRepository:

    def find_user_cards(self) -> List[Card]:
        pass

    def create_user_card(self, logged_in_user: User) -> None:
        pass

