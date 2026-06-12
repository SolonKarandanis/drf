import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from .models import NotificationEventType, NotificationStatus
from .notification_repository import NotificationRepository

logger = logging.getLogger('django')
notification_repo = NotificationRepository()


class NotificationService:

    def notify_order_event(
        self,
        event_type: NotificationEventType,
        buyer,
        supplier,
        payload: dict,
    ) -> None:
        channel_layer = get_channel_layer()
        for recipient in (buyer, supplier):
            event = notification_repo.create_notification(
                event_type=event_type,
                recipient=recipient,
                payload=payload,
            )
            group_name = f'notification_{recipient.uuid}'
            message = {
                'id': event.id,
                'event_type': event.event_type,
                'payload': event.payload,
                'created_at': event.created_at.isoformat(),
            }
            try:
                async_to_sync(channel_layer.group_send)(
                    group_name,
                    {'type': 'send_notification', 'message': message},
                )
                event.status = NotificationStatus.SENT
                event.sent_at = timezone.now()
            except Exception:
                logger.exception('Failed to push notification %s to %s', event.id, recipient.uuid)
                event.status = NotificationStatus.FAILED
            event.save(update_fields=['status', 'sent_at'])


notification_service = NotificationService()
