# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-03 10:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='star_rating',
            field=models.SmallIntegerField(blank=True),
        ),
    ]
