# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_remove_equipment_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='create_time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Create time'),
        ),
    ]
