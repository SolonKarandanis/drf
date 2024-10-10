# Generated by Django 5.1.2 on 2024-10-10 11:56

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0059_alter_attribute_type_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='type',
            field=models.CharField(choices=[('attribute.type.single', 'Single'), ('attribute.type.multiple', 'Multiple')], db_default='attribute.type.single', max_length=40),
        ),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bb37195d-cbe6-48d6-a82e-c43b91509ce0')),
        ),
    ]
