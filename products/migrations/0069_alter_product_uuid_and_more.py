# Generated by Django 5.1.2 on 2024-10-23 04:54

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0068_alter_product_uuid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c8e6f661-cfce-4ad1-b832-db1b48b0f438')),
        ),
        migrations.AlterField(
            model_name='productattributevalues',
            name='attribute_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productattributevalues',
            name='attribute_value_method',
            field=models.CharField(blank=True, default=None, max_length=120, null=True),
        ),
    ]
