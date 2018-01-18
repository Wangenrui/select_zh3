# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-07 01:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170206_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='company_reg_type',
            field=models.CharField(default=django.utils.timezone.now, max_length=32, verbose_name='Company Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.CharField(default=django.utils.timezone.now, max_length=255, verbose_name='Company Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='latitude',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=10, verbose_name='Latitude'),
        ),
        migrations.AddField(
            model_name='company',
            name='longitude',
            field=models.DecimalField(decimal_places=7, default=0.0, max_digits=10, verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_address',
            field=models.CharField(max_length=255, verbose_name='Company Address'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_code',
            field=models.CharField(max_length=32, verbose_name='Company number'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_manager',
            field=models.CharField(max_length=32, verbose_name='Company Manager'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_manager_tel',
            field=models.CharField(max_length=32, verbose_name='Company Manager Tel'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=255, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_short_name',
            field=models.CharField(max_length=32, verbose_name='Company Short Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
