# Generated by Django 4.2.5 on 2023-12-04 07:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_alter_product_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3aa287d6-8b3c-48a1-a65f-59f0edf85255')),
        ),
    ]
