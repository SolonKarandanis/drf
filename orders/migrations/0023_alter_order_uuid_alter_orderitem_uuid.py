# Generated by Django 4.2.5 on 2024-05-24 12:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0022_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ec2ee718-13d5-4a05-8cdf-fcaee3df4a6d')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('9b13a784-0420-4af9-be51-0eb636e90cee')),
        ),
    ]
