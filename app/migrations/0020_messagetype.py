# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_sysuser_file_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=32, verbose_name='Certificate Type Name')),
            ],
        ),
    ]
