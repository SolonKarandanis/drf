# Generated by Django 4.2.5 on 2024-09-02 16:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0041_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('90b97a93-52fb-48de-975f-92b84d62e6f0')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('4a22da62-b7c5-48db-bb06-cff5121d8291')),
        ),
    ]
