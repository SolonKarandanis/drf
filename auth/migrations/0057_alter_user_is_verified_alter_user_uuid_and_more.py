# Generated by Django 5.1.2 on 2024-10-10 03:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0056_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(db_default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('356b1915-949b-4a80-9b0b-498d816292d8')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='is_verified',
            field=models.BooleanField(db_default=False),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('356b1915-949b-4a80-9b0b-498d816292d8')),
        ),
    ]
