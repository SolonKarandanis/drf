from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
app = Celery('cfehome')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Athens')
app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'send-mail': {
        'task': 'mail_app.tasks.send_mail_task',
        'scheduled': crontab(hour='8', minute='52'),
        'args': (2)
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request}')
