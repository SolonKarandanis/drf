# Generated by Django 5.1.2 on 2024-10-21 05:36

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0057_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('13b0c968-a0fb-4f36-b101-003b77b7682c')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ad1b0a4c-0acf-4141-a129-4c0bc5ec3f3c')),
        ),
    ]