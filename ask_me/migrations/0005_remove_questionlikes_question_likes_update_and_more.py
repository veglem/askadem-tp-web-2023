# Generated by Django 4.2.7 on 2023-11-12 18:30

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_me', '0004_remove_questionlikes_question_likes_update_and_more'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='questionlikes',
            name='question_likes_update',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='questionlikes',
            trigger=pgtrigger.compiler.Trigger(name='question_likes_update', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n            UPDATE ask_me_question\n            SET likes = likes + 1\n            WHERE id = NEW.question_id;\n            RETURN NEW;\n        ', hash='9f05216fc9acc1401e12c0e1728f878438293f7a', operation='INSERT', pgid='pgtrigger_question_likes_update_5d969', table='ask_me_questionlikes', when='BEFORE')),
        ),
    ]
