# Generated by Django 5.1.2 on 2025-01-13 09:22

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0079_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('7709534c-c101-4542-9f9d-e0badf22cbb4')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('7709534c-c101-4542-9f9d-e0badf22cbb4')),
        ),
    ]
