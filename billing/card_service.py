import logging
from typing import List

from auth.models import User
from billing.card_repository import CardRepository
from billing.models import Card

logger = logging.getLogger('django')

card_repo = CardRepository()


class CardService:

    def find_user_cards(self, user_id: int) -> List[Card]:
        return card_repo.find_user_cards(user_id)
