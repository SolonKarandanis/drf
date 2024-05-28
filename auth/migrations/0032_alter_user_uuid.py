# Generated by Django 4.2.5 on 2024-05-24 12:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0031_alter_user_uuid_alter_userdetails_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b9c3b6c6-7297-4816-a1b5-7e57223eea98')),
        ),
    ]