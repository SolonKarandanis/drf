# Generated by Django 4.2.5 on 2023-11-30 12:53

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_uuid_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('b1bfc2ce-1e63-467d-a6e6-a845ac7feeee')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3aa57d38-2d14-41ea-968c-f1eb4171e1f8')),
        ),
        migrations.AddIndex(
            model_name='orderitem',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('product_name', config='english'), name='s_order_item_product_name_idx'),
        ),
    ]
