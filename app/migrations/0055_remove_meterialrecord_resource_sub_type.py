# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 14:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20170227_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meterialrecord',
            name='resource_sub_type',
        ),
    ]
