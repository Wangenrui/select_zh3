#coding=utf-8

from django import forms
from models import File,File1,File2


class LoginForm(forms.Form):
    user_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"用户名"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':"密码"}))


class RoleForm(forms.Form):
    role_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':"角色名称",
                                                              'name':"txt_departmentname", 'id':"txt_departmentname"}))


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ['file_position']


class FileForm1(forms.ModelForm):

    class Meta:
        model = File1
        fields = ['name']

class FileForm2(forms.ModelForm):

    class Meta:
        model = File2
        fields = ['name']
