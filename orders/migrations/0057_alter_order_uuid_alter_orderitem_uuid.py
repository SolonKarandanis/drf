# Generated by Django 5.1.2 on 2024-10-10 12:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0056_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8a3cf2cf-700e-49a8-adb3-9b213c135d49')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('80e4b5b0-f5ff-4a9f-8e78-2d013525157d')),
        ),
    ]
