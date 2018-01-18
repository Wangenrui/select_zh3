# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 11:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlastRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brole_current_state', models.CharField(max_length=2, verbose_name='\u542f\u7528\u72b6\u6001')),
                ('brole_is_login', models.BooleanField(verbose_name='\u767b\u5f55\u72b6\u6001')),
                ('brole_reg_status', models.CharField(max_length=1, verbose_name='\u6ce8\u518c\u72b6\u6001')),
                ('brole_work_status', models.CharField(max_length=1, verbose_name='\u5de5\u4f5c\u72b6\u6001')),
                ('brole_supervisor', models.CharField(max_length=2, verbose_name='\u76d1\u7406')),
                ('brole_supervisor_code', models.CharField(max_length=25, verbose_name='\u76d1\u7406\u8bc1\u4e66\u53f7')),
                ('brole_describe', models.CharField(max_length=30, verbose_name='\u5907\u6ce8')),
                ('brole_file', models.TextField(blank=True, null=True, verbose_name='\u9644\u4ef6')),
                ('brole_cert', models.CharField(max_length=25, null=True, verbose_name='\u8bc1\u4e66\u7f16\u53f7')),
            ],
        ),
        migrations.CreateModel(
            name='BlastRoleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brt_name', models.CharField(max_length=10, verbose_name='Blast Role Type Name')),
            ],
        ),
        migrations.CreateModel(
            name='CertificateType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cert_name', models.CharField(max_length=10, verbose_name='Certificate Type Name')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_name', models.CharField(max_length=100, verbose_name='City Name')),
                ('short_name', models.CharField(max_length=100, verbose_name='Short City Name')),
                ('longitude', models.DecimalField(decimal_places=7, default=0.0, max_digits=10, verbose_name='Longitude')),
                ('latitude', models.DecimalField(decimal_places=7, default=0.0, max_digits=10, verbose_name='Latitude')),
                ('sort', models.SmallIntegerField(default=0, verbose_name='Sorting Order')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30, verbose_name='Company Name')),
                ('company_short_name', models.CharField(max_length=10, verbose_name='Company Short Name')),
                ('company_code', models.CharField(max_length=10, verbose_name='Company number')),
                ('company_manager', models.CharField(max_length=20, verbose_name='Company Manager')),
                ('company_manager_tel', models.CharField(max_length=20, verbose_name='Company Manager Tel')),
                ('company_address', models.CharField(max_length=50, verbose_name='Company Address')),
                ('company_create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Company Create Date')),
                ('company_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.City')),
            ],
        ),
        migrations.CreateModel(
            name='CompanyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.CharField(max_length=2, unique=True, verbose_name='CompanyType ID')),
                ('type_name', models.CharField(max_length=10, verbose_name='CompanyType Name')),
            ],
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('county_name', models.CharField(max_length=100, verbose_name='County Name')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.City')),
            ],
        ),
        migrations.CreateModel(
            name='DepartOfCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart_name', models.CharField(max_length=20)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Company')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.DepartOfCompany')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_name', models.CharField(max_length=10)),
                ('menu_classify', models.CharField(max_length=10)),
                ('menu_addr', models.CharField(default='', max_length=20)),
                ('menu_icon', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('province_name', models.CharField(max_length=100, verbose_name='Province Name')),
                ('short_name', models.CharField(default='', max_length=100, verbose_name='Short Province Name')),
                ('parent_id', models.IntegerField(default=0, verbose_name='Prarent ID')),
                ('longitude', models.DecimalField(decimal_places=7, default=0.0, max_digits=10, verbose_name='Longitude')),
                ('latitude', models.DecimalField(decimal_places=7, default=0.0, max_digits=10, verbose_name='Latitude')),
                ('sort', models.SmallIntegerField(default=0, verbose_name='Sorting Order')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=10, verbose_name='Role Name')),
                ('menu', models.ManyToManyField(to='app.Menu')),
            ],
        ),
        migrations.CreateModel(
            name='SysUser',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=20, unique=True, verbose_name='user login id')),
                ('password', models.CharField(max_length=200)),
                ('company', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Company')),
            ],
        ),
        migrations.CreateModel(
            name='UserOfDepart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_manager', models.BooleanField(default=False)),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.DepartOfCompany')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SysUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usertype_name', models.CharField(max_length=10, verbose_name='User name')),
            ],
        ),
        migrations.AddField(
            model_name='sysuser',
            name='user_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.UserType'),
        ),
        migrations.AddField(
            model_name='role',
            name='sysuser',
            field=models.ManyToManyField(to='app.SysUser'),
        ),
        migrations.AddField(
            model_name='company',
            name='company_county',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.County'),
        ),
        migrations.AddField(
            model_name='company',
            name='company_province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Province'),
        ),
        migrations.AddField(
            model_name='company',
            name='company_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CompanyType', to_field='type_id'),
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Province'),
        ),
        migrations.AddField(
            model_name='blastrole',
            name='brole_cert_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.CertificateType'),
        ),
        migrations.AddField(
            model_name='blastrole',
            name='brole_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.BlastRoleType'),
        ),
        migrations.AddField(
            model_name='blastrole',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.SysUser', to_field='user_id'),
        ),
    ]
