# Generated by Django 5.1.2 on 2025-01-13 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_alter_card_is_active_alter_card_is_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration_year',
            field=models.IntegerField(choices=[(2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029)]),
        ),
    ]
