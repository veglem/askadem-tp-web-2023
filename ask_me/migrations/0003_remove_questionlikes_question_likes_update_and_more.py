# Generated by Django 4.2.7 on 2023-11-12 15:26

from django.db import migrations
import pgtrigger.compiler
import pgtrigger.migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ask_me', '0002_questionlikes_question_likes_update'),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name='questionlikes',
            name='question_likes_update',
        ),
        pgtrigger.migrations.AddTrigger(
            model_name='questionlikes',
            trigger=pgtrigger.compiler.Trigger(name='question_likes_update', sql=pgtrigger.compiler.UpsertTriggerSql(func='\n            UPDATE ask_me_question\n            SET likes = likes + 1\n            WHERE id = NEW.question_id;\n            RETURN NEW;\n        ', hash='736b40dff3af76c191aca0bb3547a55942a76755', level='STATEMENT', operation='INSERT', pgid='pgtrigger_question_likes_update_5d969', table='ask_me_questionlikes', when='AFTER')),
        ),
    ]
