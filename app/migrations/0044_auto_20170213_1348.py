# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 13:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_equipment_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='valid_time',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Valid time'),
        ),
    ]