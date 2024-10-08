# Generated by Django 5.1.2 on 2024-10-10 11:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0060_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('118df9ff-0e75-488e-9522-127bce72cab6')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ece4294c-023f-4ffc-9467-9cab66586fb5')),
        ),
    ]
