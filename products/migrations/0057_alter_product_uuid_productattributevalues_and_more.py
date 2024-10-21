# Generated by Django 5.1.2 on 2024-10-10 09:04

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0056_remove_attribute_value_attribute_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('a97b8d8e-d83c-4bde-8c10-414a5c6485d5')),
        ),
        migrations.CreateModel(
            name='ProductAttributeValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value_method', models.CharField(default=None, max_length=120)),
                ('attribute_value', models.FloatField()),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.attribute')),
                ('attribute_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.attributeoptions')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(through='products.ProductAttributeValues', to='products.attribute'),
        ),
    ]