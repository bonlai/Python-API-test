# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-15 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0027_auto_20180314_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendedrate',
            name='distance_rate',
            field=models.IntegerField(default=0),
        ),
    ]
