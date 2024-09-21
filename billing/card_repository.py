import logging
from typing import List

from billing.models import Card

logger = logging.getLogger('django')


class CardRepository:

    def find_user_cards(self) -> List[Card]:
        pass

