# Generated by Django 4.2.5 on 2023-12-04 07:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0013_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('70241caf-3cec-444f-b7e8-15353df44138')),
        ),
    ]
