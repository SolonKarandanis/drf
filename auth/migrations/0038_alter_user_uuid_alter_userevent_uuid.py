# Generated by Django 4.2.5 on 2024-06-05 13:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0037_alter_user_uuid_alter_userevent_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('555def51-0766-47fa-a575-df5ef2769f2b')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('555def51-0766-47fa-a575-df5ef2769f2b')),
        ),
    ]
