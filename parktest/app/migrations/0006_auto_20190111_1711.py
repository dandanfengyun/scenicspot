# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-01-11 09:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_superuser_email'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SuperUser',
            new_name='SuperAdmin',
        ),
    ]