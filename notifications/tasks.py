import logging

from celery import shared_task
from channels.layers import get_channel_layer
from .models import BroadcastNotification
import json
from celery.exceptions import Ignore
import asyncio

logger = logging.getLogger('django')


@shared_task(bind=True, autoretry_for=Exception, retry_backoff=True, retry_kwargs={'max_retries': 7})
def broadcast_notification(self, data):
    print(data)
    try:
        notification = BroadcastNotification.objects.filter(id=int(data))
        if len(notification) > 0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_broadcast",
                {
                    'type': 'send_notification',
                    'message': json.dumps(notification.message),
                }))
            notification.sent = True
            notification.save()
            return 'Done'

        else:
            logger.error('broadcast_notification task failed')
            self.update_state(
                state='FAILURE',
                meta={'exe': "Not Found"}
            )

            raise Ignore()

    except Exception as e:
        logger.error('broadcast_notification task failed')
        self.update_state(
            state='FAILURE',
            meta={
                'exe': "Failed"
                # 'exc_type': type(ex).__name__,
                # 'exc_message': traceback.format_exc().split('\n')
                # 'custom': '...'
            }
        )

        raise Ignore()
