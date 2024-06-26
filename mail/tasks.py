import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger('django')


@shared_task(bind=True, autoretry_for=Exception, retry_backoff=True, retry_kwargs={'max_retries': 7})
def send_mail_task(self, data):
    logger.info('STARTED SEND MAIL TASK')
    users = get_user_model().objects.all()
    usernames = [user.username for user in users]
    comma_seperated_usernames = ','.join(usernames)
    logger.info(f" SENDING MAIL TO USERS: {comma_seperated_usernames}")
    for user in users:
        mail_subject = "Testing"
        message = "Hey"
        to_email = user.email
        try:
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=True
            )
            return "Done"
        except Exception as e:
            logger.error('broadcast_notification task failed')


