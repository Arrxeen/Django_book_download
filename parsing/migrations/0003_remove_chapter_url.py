# Generated by Django 5.0.7 on 2025-01-26 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parsing', '0002_alter_chapter_options_chapter_falls_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='url',
        ),
    ]
