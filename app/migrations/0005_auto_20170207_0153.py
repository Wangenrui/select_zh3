# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 01:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170207_0151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='description',
            new_name='company_description',
        ),
    ]
