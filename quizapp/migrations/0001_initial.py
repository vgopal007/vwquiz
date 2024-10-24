# Generated by Django 5.1.1 on 2024-10-14 11:53

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('topic', models.CharField(blank=True, max_length=100, null=True)),
                ('question_type', models.CharField(choices=[('RB', 'Radio Button'), ('CB', 'Checkbox'), ('IN', 'Input')], default='RB', max_length=10)),
                ('question', models.CharField(max_length=100)),
                ('marks', models.IntegerField(default=1)),
                ('answer_explanation', models.CharField(blank=True, max_length=255, null=True)),
                ('difficulty_level', models.CharField(blank=True, max_length=20, null=True)),
                ('reference', models.CharField(max_length=100)),
                ('source', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuizSession',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('user', models.CharField(max_length=100)),
                ('quiz', models.CharField(max_length=100)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('completed', models.BooleanField(default=False)),
                ('timed_out', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('subject_name', models.CharField(max_length=100)),
                ('domain', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('answer', models.CharField(max_length=100)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answer', to='quizapp.question')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Topics',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('topic', models.CharField(max_length=100)),
                ('weight_perc', models.IntegerField(default=1)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types_topic', to='quizapp.types')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types_question', to='quizapp.types'),
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('selected_answer', models.CharField(max_length=200)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_user', to='quizapp.question')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quizapp.quizsession')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
