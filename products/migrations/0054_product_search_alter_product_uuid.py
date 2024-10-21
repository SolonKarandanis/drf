# Generated by Django 5.1.2 on 2024-10-10 04:40

import django.contrib.postgres.search
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0053_alter_product_public_alter_product_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='search',
            field=models.GeneratedField(db_persist=True, expression=django.contrib.postgres.search.SearchVector('sku', 'title', config='english'), output_field=django.contrib.postgres.search.SearchVectorField()),
        ),
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c9d89200-ed50-47cd-b2cc-335fd412c9e2')),
        ),
    ]