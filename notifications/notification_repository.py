from typing import List
from django.conf import settings
from django.utils import timezone
from .models import NotificationEvent, NotificationEventType

User = settings.AUTH_USER_MODEL


class NotificationRepository:

    def create_notification(
        self,
        event_type: NotificationEventType,
        recipient: User,
        payload: dict,
    ) -> NotificationEvent:
        return NotificationEvent.objects.create(
            event_type=event_type,
            recipient=recipient,
            payload=payload,
        )

    def find_unread_for_user(self, user: User):
        return (
            NotificationEvent.objects
            .filter(recipient=user, read_at__isnull=True)
            .order_by('-created_at')
        )

    def count_unread_for_user(self, user: User) -> int:
        return NotificationEvent.objects.filter(
            recipient=user, read_at__isnull=True
        ).count()

    def mark_as_read(self, user: User, ids: List[int]) -> None:
        NotificationEvent.objects.filter(
            recipient=user, id__in=ids
        ).update(read_at=timezone.now())
