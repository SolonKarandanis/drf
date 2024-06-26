# Generated by Django 4.2.5 on 2024-03-04 06:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('4f3cdadd-f6ba-40aa-a6ca-f03cc85f9ef6')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('97b90f8e-0df5-4978-bc93-cbc41c6ca983')),
        ),
    ]
