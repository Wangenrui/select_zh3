# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 08:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_remove_equipment_equipment_sub_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EquipmntSubType',
            new_name='EquipmentSubType',
        ),
    ]