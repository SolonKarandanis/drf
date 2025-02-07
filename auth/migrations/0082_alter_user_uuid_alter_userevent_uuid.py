# Generated by Django 5.1.5 on 2025-02-07 05:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0081_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9126ac5f-8eba-48be-826f-83d3cf7de6d4')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9126ac5f-8eba-48be-826f-83d3cf7de6d4')),
        ),
    ]
