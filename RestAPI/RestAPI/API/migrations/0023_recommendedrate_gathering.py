# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-07 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0022_recommendedrate_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendedrate',
            name='gathering',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='recommend', to='API.Gathering'),
            preserve_default=False,
        ),
    ]
