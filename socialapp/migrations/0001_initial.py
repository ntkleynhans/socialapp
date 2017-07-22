# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-22 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(verbose_name='published date')),
                ('user', models.CharField(max_length=32)),
                ('resource_link', models.CharField(max_length=128)),
                ('post_type', models.CharField(max_length=32)),
            ],
        ),
    ]
