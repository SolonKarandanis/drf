# Generated by Django 5.1.2 on 2024-11-19 09:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0072_rename_promo_end_discount_discount_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('6c26a9cd-a42b-4242-8eaf-9c72df0ac076')),
        ),
    ]
