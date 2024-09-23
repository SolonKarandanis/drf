# Generated by Django 4.2.5 on 2024-09-21 07:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0054_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6938b201-e371-4346-a9ea-f92b7250a932')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6938b201-e371-4346-a9ea-f92b7250a932')),
        ),
    ]