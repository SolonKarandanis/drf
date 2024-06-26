# Generated by Django 4.2.5 on 2024-05-24 12:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0030_alter_user_uuid_alter_userdetails_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ad09b1e3-42c9-468c-a822-d9eb1506152b')),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='user_details', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
