# Generated by Django 4.2.16 on 2024-11-26 15:56

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0006_topiclesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topiclesson',
            name='text_content',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]