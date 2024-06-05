# Generated by Django 4.2.5 on 2024-06-05 13:32

from django.db import migrations, models
import pgtrigger.compiler
import pgtrigger.migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0038_alter_user_uuid_alter_userevent_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3d08d8ea-02c1-4adf-942f-309cfc63eb1e')),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='uuid',
            field=models.UUIDField(default=uuid.UUID('3d08d8ea-02c1-4adf-942f-309cfc63eb1e')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='user',
            trigger=pgtrigger.compiler.Trigger(name='pgtrigger_softdelete_is_active', sql=pgtrigger.compiler.UpsertTriggerSql(func='UPDATE "custom_auth_user" SET is_active = False WHERE "id" = OLD."id"; RETURN NULL;', hash='74eccfc4c51e722572c5806632c339cf9578090d', operation='DELETE', pgid='pgtrigger_pgtrigger_softdelete_is_active_f78ab', table='custom_auth_user', when='BEFORE')),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='user',
            trigger=pgtrigger.compiler.Trigger(name='pgtrigger_softdelete_status', sql=pgtrigger.compiler.UpsertTriggerSql(func='UPDATE "custom_auth_user" SET status = \'user.deleted\' WHERE "id" = OLD."id"; RETURN NULL;', hash='3a20412f1d4154bf7f1576e62622e5c472c47073', operation='DELETE', pgid='pgtrigger_pgtrigger_softdelete_status_a6571', table='custom_auth_user', when='BEFORE')),
        ),
    ]
