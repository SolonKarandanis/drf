# Generated by Django 4.2.5 on 2024-07-03 05:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0043_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('cb865236-b631-49a7-8c7b-dca03094b89d')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('cb865236-b631-49a7-8c7b-dca03094b89d')),
        ),
    ]
