# Generated by Django 4.2.5 on 2024-05-24 12:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('ee620cdf-959f-472c-8a6f-75e7cfba6fc8')),
        ),
    ]
