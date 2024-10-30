# Generated by Django 5.1.2 on 2024-10-30 13:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0075_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3ab1a21c-d1d8-46b2-b69a-eb27c1dc67b5')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3ab1a21c-d1d8-46b2-b69a-eb27c1dc67b5')),
        ),
    ]
