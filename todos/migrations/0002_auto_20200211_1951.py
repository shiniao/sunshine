# Generated by Django 2.2.7 on 2020-02-11 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='content',
            new_name='description',
        ),
    ]
