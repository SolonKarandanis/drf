# Generated by Django 4.2.5 on 2023-11-11 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(condition=models.Q(('is_shipped', False)), fields=['id'], name='unshipped_orders'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user_id'], name='order_user_id'),
        ),
        migrations.AddConstraint(
            model_name='order',
            constraint=models.UniqueConstraint(condition=models.Q(('is_shipped', False)), fields=('user_id', 'is_shipped'), name='limit_pending_orders'),
        ),
    ]