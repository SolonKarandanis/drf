# Generated by Django 4.2.5 on 2024-06-02 14:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f9e1dfef-a1a0-4563-903f-fe3d36ca49d1')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('e17895b5-3705-4a93-9e4b-acac9a280cc0')),
        ),
    ]