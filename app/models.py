# coding=utf-8

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
import django.utils.timezone as timezone
import uuid

# Create your models here.
class UserType(models.Model):
    usertype_name = models.CharField('User name', max_length=10)


class CompanyType(models.Model):
    type_id = models.CharField('CompanyType ID', max_length=2, unique=True)
    type_name = models.CharField('CompanyType Name', max_length=10)

    def __unicode__(self):
        return self.type_id


class Province(models.Model):
    province_name = models.CharField('Province Name', max_length=100)
    short_name = models.CharField('Short Province Name', max_length=100, default='')
    parent_id = models.IntegerField('Prarent ID', default=0)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    sort = models.SmallIntegerField('Sorting Order', default=0)


class City(models.Model):
    province = models.ForeignKey(Province)
    city_name = models.CharField('City Name', max_length=100)
    short_name = models.CharField('Short City Name', max_length=100, default='')
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    sort = models.SmallIntegerField('Sorting Order', default=0)


class County(models.Model):
    city = models.ForeignKey(City)
    county_name = models.CharField('County Name', max_length=100)
    short_name = models.CharField('Short City Name', max_length=100, default='')
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    sort = models.SmallIntegerField('Sorting Order', default=0)


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    company_create_time = models.DateTimeField('Company Create Date', default=timezone.now)
    company_province = models.ForeignKey(Province)
    company_city = models.ForeignKey(City)
    company_county = models.ForeignKey(County)
    company_name = models.CharField('Company Name', max_length=255)
    company_type = models.ForeignKey(CompanyType,to_field='type_id')
    company_short_name = models.CharField('Company Short Name', max_length=32)
    company_code = models.CharField('Company number', max_length=32)
    company_manager = models.CharField('Company Manager', max_length = 32)
    company_manager_tel = models.CharField('Company Manager Tel', max_length=32)
    company_address = models.CharField('Company Address', max_length=255)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    company_description = models.CharField('Company Address', max_length=255)
    company_reg_type = models.CharField('Company Address', max_length=32, null=True)

    def __unicode__(self):
        return self.company_name


class FileType(models.Model):
    filetype_name = models.CharField('File type name', max_length=32)


class SexType(models.Model):
    sex_type = models.CharField('Sex type name', max_length=8)


class CertificateType(models.Model):
    cert_name = models.CharField('Certificate Type Name', max_length=10)

    def __unicode__(self):
        return self.cert_name


class MessageType(models.Model):
    message_type = models.CharField('Message Type Name', max_length=32)

    def __unicode__(self):
        return self.message_type


class SysUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user_type = models.ForeignKey(UserType, default=1)
    company = models.ForeignKey(Company, null=True, default=None)
    user_id = models.CharField('User login id', max_length = 20, unique=True)
    password = models.CharField(max_length=256)
    user_name = models.CharField('User name', max_length = 20, default='')
    fullname = models.CharField('User full name', max_length = 64, default='')
    id_card = models.CharField('User ID card number', max_length = 32, default='')
    sex = models.TextField('Set type', max_length=32, null=True, default='')
    photo = models.ImageField('Photo', null=True)
    email = models.CharField('E-mail', max_length=45, null=True, default='')
    telephone = models.CharField('Telephone number', max_length=32, null=True, default='')
    address = models.CharField('Address', max_length=128, null=True, default='')
    reg_status = models.SmallIntegerField('Registration Status', default=1)
    is_login = models.BooleanField('Is login user', default=True)
    is_supervisor = models.BooleanField('Is supervisor', default=False)
    work_status = models.SmallIntegerField('Current Status', default=1)
    current_status = models.SmallIntegerField('Current Status', default=0)
    burst_code = models.TextField('Burst Code', max_length=32, default='')
    supervisor_id = models.CharField('Address', max_length=128, null=True, default='')
    describe = models.TextField('Description', null=True, default='')
    certificate_type = models.ForeignKey(CertificateType, null=True, default=None)
    file_kit = models.CharField('File Kit', max_length=128, null=True, default='')
    file_name = models.CharField('File Name', max_length=256, null=True, default='')
    message_type = models.ForeignKey(MessageType, default=1)

    def __str__(self):
        return self.user_name

    def __unicode__(self):
        return self.user_name


class FileKit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    user = models.UUIDField('Apply User Id', null=True, default=None)
    apply_user = models.UUIDField('Apply User Id', null=True, default=None)
    company = models.UUIDField('Company Id', null=True, default=None)
    filetype = models.ForeignKey(FileType, default=1)
    code = models.CharField('File code', max_length = 64, null=True, default='')
    create_time = models.DateTimeField('File Create Date', default=timezone.now)
    content = models.TextField('Content', blank=True, null=True)


class Menu(models.Model):
    menu_name = models.CharField(max_length=10)
    menu_classify = models.CharField(max_length=10)
    menu_addr = models.CharField(max_length=20, default="")
    menu_icon = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return self.menu_name

class Role(models.Model):
    role_name = models.CharField('Role Name', max_length=10)
    sysuser = models.ManyToManyField(SysUser)
    menu = models.ManyToManyField(Menu)

    def __unicode__(self):
        return self.role_name

class BlastRoleType(models.Model):
    brt_name = models.CharField('Blast Role Type Name', max_length=10)

    def __unicode__(self):
        return self.brt_name


class BlastRole(models.Model):
    user_id = models.ForeignKey(SysUser, to_field='user_id')
    brole_type = models.ForeignKey(BlastRoleType)
    brole_cert_type = models.ForeignKey(CertificateType)
    brole_current_state = models.CharField('启用状态', max_length=2)
    brole_is_login = models.BooleanField('登录状态')
    brole_reg_status = models.CharField('注册状态', max_length=1)
    brole_work_status = models.CharField('工作状态', max_length=1)
    brole_supervisor = models.CharField('监理', max_length=2)
    brole_supervisor_code = models.CharField('监理证书号', max_length=25)
    brole_describe = models.CharField('备注', max_length=30)
    brole_file = models.TextField('附件', blank=True, null=True)
    brole_cert = models.CharField('证书编号', max_length=25, null=True)

    def __unicode__(self):
        return self.user_id


class DepartOfCompany(models.Model):
    company = models.ForeignKey(Company)
    parent = models.ForeignKey('self',null=True)
    depart_name = models.CharField(max_length=64)


class UserOfDepart(models.Model):
    depart = models.ForeignKey(DepartOfCompany)
    user = models.ForeignKey(SysUser)
    is_manager = models.BooleanField(default=False)


class EquipmentType(models.Model):
    name = models.CharField('Equipment Type', max_length=12)

    def __unicode__(self):
        return self.name


class EquipmentSubType(models.Model):
    name = models.CharField('Equipment Type', max_length=12)
    type = models.ForeignKey(EquipmentType)

    def __unicode__(self):
        return self.name


class EquipmentMode(models.Model):
    name = models.CharField('Equipment Mode', max_length=12)

    def __unicode__(self):
        return self.name


class Equipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    equipment_name = models.CharField('Equipment name', max_length = 64, null=True, default='')
    equipment_code = models.CharField('Equipment code', max_length = 64, null=True, default='')
    reg_status = models.SmallIntegerField('Register status', default=2)
    work_status = models.SmallIntegerField('Working status', default=1)
    create_time = models.DateField('Create time', default=timezone.now)
    valid_time = models.DateField('Valid time', default=timezone.now)
    allot_company_id = models.UUIDField('Allocation company id', default=uuid.uuid4, editable=True)
    company = models.ForeignKey(Company, null=True, default=None)
    equipment_sub_type = models.ForeignKey(EquipmentSubType, null=True, default=None)
    equipment_mode = models.ForeignKey(EquipmentMode, null=True, default=1)

    def __unicode__(self):
        return self.equipment_name


class WorkFlow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    state = models.CharField('State', max_length=16, default='')
    status = models.CharField('Status', max_length=16, default='')
    comment_type = models.CharField(max_length=16, default='')
    lock_mode = models.SmallIntegerField(default=0)
    b_require_select_user = models.BooleanField(default=False)
    comment_type = models.BooleanField(default=False)
    b_can_terminate = models.BooleanField(default=False)
    b_can_translate = models.BooleanField(default=False)

    def __unicode__(self):
        return self.state


class ProjectStatus(models.Model):
    name = models.CharField(max_length=32, default='')


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    county = models.ForeignKey(County)
    create_time = models.DateField('Create time', default=timezone.now)
    name = models.CharField('Name', max_length=64, null=True, default='')
    address = models.CharField('Addess', max_length=128, null=True, default='')
    describe = models.CharField(max_length=256, default='')
    apply_user = models.ForeignKey(SysUser)
    company = models.ForeignKey(Company)
    police_company_id = models.CharField('Police Company Id', max_length=32, null=True, default='')
    project_code = models.CharField('Project Code', max_length=64, null=True, default='')
    file_kit_id = models.CharField('File Kit Id', max_length=32, null=True, default='')
    work_flow = models.ForeignKey(WorkFlow, null=True, default=None)
    status = models.ForeignKey(ProjectStatus, default=2)
    associate_status = models.SmallIntegerField(default=1)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    radius = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __unicode__(self):
        return self.name


class AreaStatus(models.Model):
    name = models.CharField(max_length=32, default='')


class AreaReportStatus(models.Model):
    name = models.CharField(max_length=32, default='')


class AreaRegStatus(models.Model):
    name = models.CharField(max_length=32, default='')


class Area(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    company = models.ForeignKey(Company)
    apply_user = models.ForeignKey(SysUser)
    project = models.ForeignKey(Project)
    create_time = models.DateField('Create time', default=timezone.now)
    name = models.CharField('Name', max_length=64, null=True, default='')
    describe = models.CharField(max_length=256, default='')
    work_flow = models.ForeignKey(WorkFlow, null=True, default=None)
    equipment = models.ForeignKey(Equipment, null=True, default=None)
    status = models.ForeignKey(AreaStatus, default=1)
    report_status = models.ForeignKey(AreaReportStatus, default=1)
    reg_status = models.ForeignKey(AreaRegStatus, default=1)
    gps_longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    gps_latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    baidu_longitude = models.DecimalField('Baidu Longitude', max_digits=10, decimal_places=7, default=0.0)
    baidu_latitude = models.DecimalField('Baidu Latitude', max_digits=10, decimal_places=7, default=0.0)
    radius = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    plan_dgt_deto_num = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    plan_deto_num = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    plan_explosive_num = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)

    def __unicode__(self):
        return self.name


class BlastType(models.Model):
    name = models.CharField(max_length=32, default='')


class BlastMode(models.Model):
    name = models.CharField(max_length=32, default='')


class BlastRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    county = models.ForeignKey(County)
    police_company_id = models.CharField('Police Company Id', max_length=32, null=True, default='')
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project)
    area = models.ForeignKey(Area)
    equipment = models.ForeignKey(Equipment)
    deto_transfer_record_id = models.CharField('Deto transfer record Id', max_length=32, null=True, default='')
    user1_id = models.CharField('User1 Id', max_length=32, null=True, default='')
    user2_id = models.CharField('User2 Id', max_length=32, null=True, default='')
    blast_auth_user1_id = models.CharField('Auth User1 Id', max_length=32, null=True, default='')
    blast_auth_user2_id = models.CharField('Auth User2 Id', max_length=32, null=True, default='')
    create_time = models.DateTimeField('Create time', default=timezone.now)
    blasting_time = models.DateTimeField('Blasting time', default=timezone.now)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    blast_type = models.ForeignKey(BlastType)
    blast_mode = models.ForeignKey(BlastMode)


class SignType(models.Model):
    name = models.CharField(max_length=32, default='')


class SignRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    county = models.ForeignKey(County)
    police_company_id = models.CharField('Police Company Id', max_length=32, null=True, default='')
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project)
    area = models.ForeignKey(Area)
    equipment = models.ForeignKey(Equipment)
    supervisor_company_id = models.CharField('supervisor_company_id', max_length=32, null=True, default='')
    user = models.ForeignKey(SysUser)
    sign_type = models.ForeignKey(SignType)
    create_time = models.DateTimeField('Create time', default=timezone.now)
    sign_time = models.DateTimeField('Sign in time', default=timezone.now)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)


class ResourceType(models.Model):
    name = models.CharField(max_length=32, default='')


class Transport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    county = models.ForeignKey(County)
    police_company_id = models.CharField('Police Company Id', max_length=32, null=True, default='')
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project)
    area = models.ForeignKey(Area)
    equipment = models.ForeignKey(Equipment)
    user = models.ForeignKey(SysUser)
    resource_type = models.ForeignKey(ResourceType)
    resource_count = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    create_time = models.DateTimeField('Create time', default=timezone.now)
    transport_time = models.DateTimeField('transport_time', default=timezone.now)
    car_code = models.CharField('car_code', max_length=32, null=True, default='')


class TransferRecordType(models.Model):
    id = models.SmallIntegerField(primary_key=True, default=0, editable=True)
    name = models.CharField(max_length=32, default='')


class MaterialType(models.Model):
    id = models.SmallIntegerField(primary_key=True, default=0, editable=True)
    name = models.CharField(max_length=32, default='')


class MaterialSubType(models.Model):
    code = models.CharField(max_length=32, default='')
    name = models.CharField(max_length=32, default='')
    type = models.ForeignKey(MaterialType)
    unit_type = models.SmallIntegerField(null=True, default=0)
    prompt = models.CharField(max_length=32, null=True, default='')


class Transfer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    county = models.ForeignKey(County)
    police_company_id = models.CharField('Police Company Id', max_length=32, null=True, default='')
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project)
    area = models.ForeignKey(Area)
    equipment = models.ForeignKey(Equipment)
    from_user1_id = models.CharField('From User1 Id', max_length=32, null=True, default='')
    from_user2_id = models.CharField('From User2 Id', max_length=32, null=True, default='')
    to_user2_id = models.CharField('To User1 Id', max_length=32, null=True, default='')
    to_user1_id = models.CharField('To User2 Id', max_length=32, null=True, default='')
    record_type = models.ForeignKey(TransferRecordType)
    resource_type = models.ForeignKey(MaterialType)
    create_time = models.DateTimeField('Create time', default=timezone.now)
    transfer_time = models.DateTimeField('transfer_time', default=timezone.now)
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    resource_count = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)


class MaterialRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    record = models.ForeignKey(Transfer)
    area = models.ForeignKey(Area)
    user = models.ForeignKey(SysUser)
    record_type = models.ForeignKey(TransferRecordType)
    resource_type = models.ForeignKey(MaterialType)
    resource_sub_type = models.ForeignKey(MaterialSubType)
    main_code = models.CharField('main_code', max_length=32, null=True, default='')
    soc_code = models.CharField('soc_code', max_length=32, null=True, default='')
    produce_code = models.CharField('produce_code', max_length=32, null=True, default='')
    simple_code = models.CharField('simple_code', max_length=32, null=True, default='')
    start_index = models.IntegerField(null=True, default=0)
    end_index = models.IntegerField(null=True, default=0)
    version_id = models.SmallIntegerField(null=True, default=0)
    deto_status = models.SmallIntegerField(null=True, default=0)
    resource_count = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    unit = models.IntegerField(null=True, default=0)


class ProtectedObjectTypes(models.Model):
    name = models.CharField(max_length=32, default='')
    range_x1 = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    range_x2 = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    range_y1 = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    range_y2 = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    range_z1 = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)
    range_z2 = models.DecimalField(max_digits=10, decimal_places=3, default=0.0)


class ProjectBlastTypes(models.Model):
    name = models.CharField(max_length=32, default='')
    shake_hz_1 = models.IntegerField(default=0)
    shake_hz_2 = models.IntegerField(default=0)


class ProjectCompany(models.Model):
    project = models.ForeignKey(Project)
    company = models.ForeignKey(Company)


class ProjectPerson(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(SysUser)


class ProjectSupervisor(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(SysUser)


class VideoAccessType(models.Model):
    name = models.CharField(max_length=32, null=True, default='')


class VideoCamera(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    province = models.ForeignKey(Province)
    city = models.ForeignKey(City)
    county = models.ForeignKey(County)
    company = models.ForeignKey(Company)
    project = models.ForeignKey(Project, null=True, default='')
    area = models.ForeignKey(Area, null=True, default='')
    access_type = models.ForeignKey(VideoAccessType)
    responsible_person = models.CharField(max_length=32, null=True, default='')
    monitor_point_name = models.CharField(max_length=32, null=True, default='')
    monitor_point_address = models.CharField(max_length=128, null=True, default='')
    camera_manufacture = models.CharField(max_length=64, null=True, default='')
    contact_phone = models.CharField(max_length=64, null=True, default='')
    camera_code = models.CharField(max_length=32, null=True, default='')
    camera_type = models.CharField(max_length=32, null=True, default='')
    visit_url = models.CharField(max_length=256, null=True, default='')
    login_user_name = models.CharField(max_length=32, null=True, default='')
    login_password = models.CharField(max_length=32, null=True, default='')
    create_time = models.DateTimeField('Create time', default=timezone.now)
    type = models.IntegerField(null=True, default=1)
    status = models.IntegerField(null=True, default=1)


class Finger(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    finger_data = models.TextField(max_length=2048, null=True, default='')
    user = models.ForeignKey(SysUser)


class Seismometer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    area = models.ForeignKey(Area, null=True, default='')
    user = models.ForeignKey(SysUser)
    project_blast_type = models.ForeignKey(ProjectBlastTypes)
    protected_obj_type = models.ForeignKey(ProtectedObjectTypes)
    protected_obj_distance = models.IntegerField(null=True, default=0)
    blast_transmission_v = models.IntegerField(null=True, default=0)
    blast_shake_hz = models.IntegerField(null=True, default=0)
    create_time = models.DateTimeField('Create time', default=timezone.now)


class DetonatorStatus(models.Model):
    name = models.CharField(max_length=32, null=True, default='')


class DigitalDetonator(models.Model):
    equipment = models.ForeignKey(Equipment, null=True, default='')
    area = models.ForeignKey(Area, null=True, default='')
    user = models.ForeignKey(SysUser, null=True, default='')
    longitude = models.DecimalField('Longitude', max_digits=10, decimal_places=7, default=0.0)
    latitude = models.DecimalField('Latitude', max_digits=10, decimal_places=7, default=0.0)
    blast_time = models.DateTimeField('Blast time', default=timezone.now)
    code = models.CharField('Code', max_length=32, null=True, default='')
    company_code = models.CharField('Company Code', max_length=10, null=True, default='')
    special_code = models.CharField('Special Code', max_length=10, null=True, default='')
    serial_code = models.CharField('Serial Code', max_length=10, null=True, default='')
    manu_date = models.DateField('Manu Date', default=timezone.now)
    status = models.ForeignKey(DetonatorStatus, null=True, default='')
    create_time = models.DateTimeField('Create time', default=timezone.now)


class NormalUser(models.Model):
    username = models.CharField(max_length=30)
    headImg = models.FileField(upload_to='./upload')

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ['username']


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    subject = models.CharField(max_length=100)
    file_position = models.FileField(upload_to='./upload', verbose_name='文件名称')
    filename = models.CharField(max_length=100)
    def __unicode__(self):
        return self.file_position
class File2(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.FileField(upload_to='./upload', verbose_name='文件名称')

    def __unicode__(self):
        return self.name
class File1(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.FileField(upload_to='./upload', verbose_name='文件名称')

    def __unicode__(self):
        return self.name



##
##

class Major(models.Model):
    id = models.AutoField(primary_key=True)
    major=models.CharField(max_length=64)

class Select_Role(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=10)


class Sex(models.Model):
    id = models.AutoField(primary_key=True)
    sex = models.CharField(max_length=10)

class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    institution_name = models.CharField(max_length=30)

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=10)

class select_sysUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    role = models.ForeignKey(Select_Role)
    password = models.CharField(max_length=256)
    sex = models.ForeignKey(Sex)
    stu_class = models.CharField(max_length=30)
    tel = models.CharField(max_length=30)
    achieve_year = models.PositiveSmallIntegerField()
    institution = models.ForeignKey(Institution)
    major = models.ForeignKey(Major)
    score = models.CharField(max_length=64)



    #menu = models.ManyToManyField(Menu)



class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=10)
    subject = models.CharField(max_length=64)
    tea_no = models.CharField(max_length=30)
    introduction = models.CharField(max_length=256)
    research_papers = models.CharField(max_length=20,null=True, default='')
    engineering_design = models.CharField(max_length=20, null=True, default='')
    project_report = models.CharField(max_length=20, null=True, default='')
    summary_report = models.CharField(max_length=20, null=True, default='')
    other = models.CharField(max_length=20, null=True, default='')
    other_introduction = models.CharField(max_length=256, null=True, default='')
    combine_actual = models.CharField(max_length=20, null=True, default='')
    company_name = models.CharField(max_length=30, null=True, default='')
    implementation_state = models.CharField(max_length=30, null=True, default='')
    english_title = models.CharField(max_length=256)
    subject_property = models.CharField(max_length=20, null=True, default='')
    major = models.ForeignKey(Major)

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    stu_no = models.CharField(max_length=30)
    volunteer_topic_no = models.ForeignKey(Topic)
    success = models.CharField(max_length=10)
    submit = models.CharField(max_length=10)
    volunteer_no = models.PositiveIntegerField()


class Application_state(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.CharField(max_length=64)
    selected_stu_no = models.CharField(max_length=30)
    submit=models.CharField(max_length=11)


class Stu_introduction(models.Model):
    id = models.AutoField(primary_key=True)
    stu_no = models.CharField(max_length=30)
    stu_introduction = models.CharField(max_length=256)

class selectFile(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=64)
    files = models.CharField(max_length=64)
    file_position = models.FileField(upload_to='./upload', verbose_name='文件名称')

class Date_setting(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=30)
    av_start = models.CharField(max_length=30)
    av_end = models.CharField(max_length=30)
    write_sub_s = models.CharField(max_length=30)
    write_sub_e = models.CharField(max_length=30)
    select1_start = models.CharField(max_length=30)
    select1_end = models.CharField(max_length=30)
    select2_start = models.CharField(max_length=30)
    select2_end = models.CharField(max_length=30)
    select3_start = models.CharField(max_length=30)
    select3_end = models.CharField(max_length=30)
    superintendent_s = models.CharField(max_length=30)
    superintendent_e = models.CharField(max_length=30)
    end_select = models.CharField(max_length=30)
    upload_s = models.CharField(max_length=30)
    upload_e = models.CharField(max_length=30)
    activation = models.CharField(max_length=10)

class Select_num_datem(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.PositiveIntegerField()
    select_num = models.PositiveIntegerField()
    start_date = models.DateField(max_length=30)
    end_date = models.DateField(max_length=30)

class Teacher_topic_num(models.Model):
    id = models.AutoField(primary_key=True)
    tea_no = models.CharField(max_length=30)
    topic_num = models.CharField(max_length=10)
    year = models.CharField(max_length=20)

        ##

class institution_topic_num(models.Model):
    id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution)
    max = models.CharField(max_length=32)
    min = models.CharField(max_length=32)
    year = models.CharField(max_length=32)
    automation = models.CharField(max_length=32)
    measurement = models.CharField(max_length=32)
    electrical = models.CharField(max_length=32)
    electronic = models.CharField(max_length=32)

class giveup_topic(models.Model):
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic)
    day_num = models.CharField(max_length=32)

class Topic1(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=10)
    subject = models.CharField(max_length=64)
    tea_no = models.CharField(max_length=30)
    introduction = models.CharField(max_length=256)
    research_papers = models.CharField(max_length=20,null=True, default='')
    engineering_design = models.CharField(max_length=20, null=True, default='')
    project_report = models.CharField(max_length=20, null=True, default='')
    summary_report = models.CharField(max_length=20, null=True, default='')
    other = models.CharField(max_length=20, null=True, default='')
    other_introduction = models.CharField(max_length=256, null=True, default='')
    combine_actual = models.CharField(max_length=20, null=True, default='')
    company_name = models.CharField(max_length=30, null=True, default='')
    implementation_state = models.CharField(max_length=30, null=True, default='')
    english_title = models.CharField(max_length=256)
    subject_property = models.CharField(max_length=20, null=True, default='')
    major = models.ForeignKey(Major)
    topic = models.CharField(max_length=20, null=True, default='')



