# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-10 01:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170209_1211'),
    ]

    operations = [
        migrations.AddField(
            model_name='sysuser',
            name='file_name',
            field=models.CharField(default='', max_length=256, verbose_name='File Name'),
        ),
    ]
