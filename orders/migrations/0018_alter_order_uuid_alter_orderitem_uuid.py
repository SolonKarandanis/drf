# Generated by Django 4.2.5 on 2024-05-23 12:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_order_uuid_alter_orderitem_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('c65afc93-1bf5-420b-bf9b-1cf67085e77d')),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('2dc9df6c-dfd5-431e-b1ea-6776c3def501')),
        ),
    ]
