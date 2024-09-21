# Generated by Django 4.2.5 on 2024-09-21 07:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0051_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8d0da5c1-c517-4fd6-9d56-2a7ac57ab2b4')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8d0da5c1-c517-4fd6-9d56-2a7ac57ab2b4')),
        ),
    ]
