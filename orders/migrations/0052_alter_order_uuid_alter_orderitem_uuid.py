# Generated by Django 5.1.2 on 2024-10-10 08:48

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0051_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('2943c8c9-6fa1-49f8-983e-2a3f10f5dd83')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('16ceaf6d-1da9-492f-bbff-7e5b1986905f')),
        ),
    ]