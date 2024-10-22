# Generated by Django 5.1.2 on 2024-10-21 05:37

import django.contrib.postgres.search
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0062_remove_product_search_alter_product_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search',
            field=models.GeneratedField(db_persist=True, expression=django.contrib.postgres.search.SearchVector('sku', 'title', 'content', config='english'), output_field=django.contrib.postgres.search.SearchVectorField()),
        ),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('bd7f8cd3-8fe1-4e70-8ed3-676d1ac0d432')),
        ),
    ]