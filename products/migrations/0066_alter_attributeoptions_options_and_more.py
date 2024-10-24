# Generated by Django 5.1.2 on 2024-10-22 05:17

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0065_product_search_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attributeoptions',
            options={'verbose_name_plural': 'Attribute Options'},
        ),
        migrations.AlterModelOptions(
            name='productattributevalues',
            options={'verbose_name_plural': 'Product Attribute Values'},
        ),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('4cfd4ca4-3718-45b6-890d-74730e0d1b9e')),
        ),
        migrations.AlterModelTable(
            name='attributeoptions',
            table='attribute_options',
        ),
        migrations.AlterModelTable(
            name='productattributevalues',
            table='product_attribute_values',
        ),
    ]
