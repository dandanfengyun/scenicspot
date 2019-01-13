# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-11 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='superuser',
            options={'verbose_name': '超级管理员'},
        ),
        migrations.AlterField(
            model_name='superuser',
            name='phone',
            field=models.CharField(max_length=13, unique=True, verbose_name='手机'),
        ),
    ]