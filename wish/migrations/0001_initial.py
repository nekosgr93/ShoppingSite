# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-05 18:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0005_product_star_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to='products.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wish_list', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
