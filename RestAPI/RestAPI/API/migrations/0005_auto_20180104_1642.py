# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-04 08:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20180104_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gathering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('start_datetime', models.DateTimeField()),
                ('is_start', models.BooleanField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.AppUser')),
            ],
            options={
                'db_table': 'gathering',
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('address', models.TextField()),
                ('self_introduction', models.TextField()),
                ('password', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'restaurant',
            },
        ),
        migrations.AddField(
            model_name='gathering',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.Restaurant'),
        ),
    ]
