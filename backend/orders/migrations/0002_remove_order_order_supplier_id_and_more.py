# Generated by Django 4.2.5 on 2023-11-28 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='order',
            name='order_supplier_id',
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(condition=models.Q(('is_shipped', False)), fields=['supplier_id'], name='order_supplier_id'),
        ),
    ]
