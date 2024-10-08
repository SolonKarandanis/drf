# Generated by Django 5.1.2 on 2024-10-10 11:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0057_alter_product_uuid_productattributevalues_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='type',
            field=models.CharField(default=None, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a45783ed-d11f-4a20-94b6-6bdfb5734537')),
        ),
    ]
