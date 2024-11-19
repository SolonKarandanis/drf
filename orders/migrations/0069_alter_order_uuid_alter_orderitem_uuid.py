# Generated by Django 5.1.2 on 2024-11-19 09:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0068_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('38b0642e-58f8-4ea5-8fb8-f7f6765a2c88')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9b40b8a6-15d5-4083-b15e-9f7713416428')),
        ),
    ]