# Generated by Django 4.2.16 on 2024-11-14 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0003_question_delete_flag_question_qc_paased'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='qc_paased',
            new_name='qc_passed',
        ),
    ]