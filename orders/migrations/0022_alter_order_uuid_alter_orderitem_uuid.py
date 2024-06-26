# Generated by Django 4.2.5 on 2024-05-24 12:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0021_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('d8060198-ebc7-4b69-bdce-a5937a32de07')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('da49e766-a993-498d-9822-6f37b645a514')),
        ),
    ]
