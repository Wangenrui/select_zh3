# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-05 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0064_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='name',
            field=models.FileField(upload_to='./upload', verbose_name='\u6587\u4ef6\u540d\u79f0'),
        ),
    ]