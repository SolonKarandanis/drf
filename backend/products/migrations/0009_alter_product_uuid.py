# Generated by Django 4.2.5 on 2023-12-04 07:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c78d4229-f4ca-479d-a8c2-882266c5c7a7')),
        ),
    ]
