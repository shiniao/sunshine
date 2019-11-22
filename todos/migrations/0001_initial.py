# Generated by Django 2.2.7 on 2019-11-22 03:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('finished', models.BooleanField(default=False)),
                ('expired', models.DateField(blank=True, null=True)),
                ('priority', models.IntegerField(default=4)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['expired'],
            },
        ),
    ]
