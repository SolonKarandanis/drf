from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import MINUTES, PeriodicTask, CrontabSchedule, PeriodicTasks
import json


class NotificationEventType(models.TextChoices):
    ORDER_CREATED = 'purchase.order.created'
    BUYER_REJECTED = 'purchase.order.buyer.rejected'
    SUPPLIER_REJECTED = 'purchase.order.supplier.rejected'
    APPROVED = 'purchase.order.approved'
    SHIPPED = 'purchase.order.shipped'
    RECEIVED = 'purchase.order.received'


class NotificationStatus(models.TextChoices):
    CREATED = 'notification.status.created'
    SENT = 'notification.status.sent'
    FAILED = 'notification.status.failed'


class NotificationEvent(models.Model):
    event_type = models.CharField(max_length=60, choices=NotificationEventType.choices)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        db_index=True,
    )
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=40,
        choices=NotificationStatus.choices,
        default=NotificationStatus.CREATED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=['recipient', 'read_at'],
                name='notification_unread_idx',
            )
        ]

    def __repr__(self):
        return f'<NotificationEvent {self.event_type} → {self.recipient_id}>'


# Create your models here.
class BroadcastNotification(models.Model):
    message = models.TextField()
    broadcast_on = models.DateTimeField()
    sent = models.BooleanField(default=False)

    class Meta:
        ordering = ['-broadcast_on']


@receiver(post_save, sender=BroadcastNotification)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    if created:
        schedule, created = CrontabSchedule.objects.get_or_create(hour=instance.broadcast_on.hour,
                                                                  minute=instance.broadcast_on.minute,
                                                                  day_of_month=instance.broadcast_on.day,
                                                                  month_of_year=instance.broadcast_on.month)
        task = PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-" + str(instance.id),
                                           task="notifications.tasks.broadcast_notification",
                                           args=json.dumps((instance.id,)))
