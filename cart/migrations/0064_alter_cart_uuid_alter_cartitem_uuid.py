# Generated by Django 5.1.2 on 2024-10-21 05:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0063_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('4a073ba8-7d20-445b-b866-471b91c9ac1a')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('79e519a2-63a1-4c54-9f6a-8ddc0a9f4aa9')),
        ),
    ]
