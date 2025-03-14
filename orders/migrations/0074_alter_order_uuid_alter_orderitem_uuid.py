# Generated by Django 5.1.5 on 2025-02-07 05:24

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0073_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('14ab7bae-d0f2-4eeb-adff-9e09ce6c5129')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('beb7b5d6-2255-4574-bdef-b1eb590a766b')),
        ),
    ]
