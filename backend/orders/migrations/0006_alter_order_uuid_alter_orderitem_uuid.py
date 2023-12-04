# Generated by Django 4.2.5 on 2023-12-04 07:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderitem_s_order_item_product_name_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('8363ade8-c9bf-49c0-821d-c480aba643c4')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('55c11959-0610-4e84-8f6d-9bd46195655a')),
        ),
    ]
