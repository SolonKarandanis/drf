# Generated by Django 4.2.5 on 2024-07-03 05:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0036_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bb280b30-ce9e-4293-91f4-ed3ba544e6cf')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('57797d91-b02e-40bd-8124-e1b54379d912')),
        ),
    ]
