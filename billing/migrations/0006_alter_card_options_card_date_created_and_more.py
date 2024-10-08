# Generated by Django 4.2.5 on 2024-09-21 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('billing', '0005_remove_card_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='card',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='card',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='CardUser',
        ),
    ]
