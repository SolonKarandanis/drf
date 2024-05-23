# Generated by Django 4.2.5 on 2023-12-18 07:49

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0015_alter_cart_uuid_alter_cartitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('304b818e-e2db-4f50-840c-41af033e0f6a')),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('2c0fd4cc-d314-4bae-958f-1f90ce68e130')),
        ),
    ]