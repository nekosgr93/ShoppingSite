# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-11 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180211_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='country',
            field=models.CharField(choices=[('China', 'China'), ('Canada', 'Canada'), ('Japan', 'Japan'), ('United Kingdom', 'United Kingdom'), ('United States', 'United States'), ('Taiwan', 'Taiwan')], max_length=50),
        ),
    ]
