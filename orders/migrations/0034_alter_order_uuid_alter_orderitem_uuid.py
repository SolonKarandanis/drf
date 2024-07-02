# Generated by Django 4.2.5 on 2024-07-02 05:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0033_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8f9c003a-a4be-4466-89f1-428bb4fa9b14')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('f56b02d5-8230-48af-9423-94a733beae88')),
        ),
    ]