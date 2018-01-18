# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-08-16 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0094_auto_20170813_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='submit',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='select_sysuser',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Select_Role'),
        ),
    ]