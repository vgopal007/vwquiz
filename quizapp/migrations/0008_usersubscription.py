# Generated by Django 4.2.16 on 2024-11-27 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizapp', '0007_alter_topiclesson_text_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateField(auto_now=True)),
                ('Active', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('expire_at', models.DateField()),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subjects', to='quizapp.types')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
