from django.contrib import admin
from app.models import SysUser,select_sysUser
from django.contrib.auth.models import User
# Register your models here.

admin.site.unregister(User)
admin.site.register(User, select_sysUser)