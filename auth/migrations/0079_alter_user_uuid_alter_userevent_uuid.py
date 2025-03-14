# Generated by Django 5.1.2 on 2025-01-13 08:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0078_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e0fd5f35-d0ad-45be-8b5e-96dc2930965b')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e0fd5f35-d0ad-45be-8b5e-96dc2930965b')),
        ),
    ]
