# Generated by Django 4.2.5 on 2024-08-22 06:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0040_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('2403d6ac-08dc-4c1d-be03-0510d9ab3f7f')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('017a4e09-ef8f-4dfa-91d5-7cfdee3d2803')),
        ),
    ]