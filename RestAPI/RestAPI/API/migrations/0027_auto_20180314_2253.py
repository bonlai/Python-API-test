# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-14 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0026_remove_recommendedrate_restaurant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilepic',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='latitude',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='longitude',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.DeleteModel(
            name='ProfilePic',
        ),
    ]
