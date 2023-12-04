# Generated by Django 4.2.5 on 2023-12-04 07:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0012_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('30a5eab0-d258-42e4-9d22-38e4960aab52')),
        ),
    ]
