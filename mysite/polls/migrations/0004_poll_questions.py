# Generated by Django 5.0.7 on 2025-01-14 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_poll_question_description_alter_choice_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='questions',
            field=models.TextField(default='[]'),
        ),
    ]