# Generated by Django 5.1.7 on 2025-04-09 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_profile_alter_question_author_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.CharField(default='question', max_length=1000),
            preserve_default=False,
        ),
    ]
