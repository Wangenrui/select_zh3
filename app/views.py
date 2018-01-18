# coding=utf-8


from django.contrib import messages
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest,Http404,HttpResponseBadRequest,HttpResponseForbidden,HttpResponseGone,HttpResponseNotAllowed,HttpResponseNotFound,HttpResponseNotModified,HttpResponsePermanentRedirect,HttpResponseServerError
from password import prpcrypt
from models import SysUser, Menu, Role, NormalUser, Company,select_sysUser,Select_Role
from form import RoleForm, LoginForm, FileForm,FileForm1,FileForm2
from . import DBoperater
from django import forms
from django.template import RequestContext
from urllib import quote
import json


pc = prpcrypt('boomboomboomboom')


def get_menu(usercode):
    print 'User Login: ' + usercode
    users = select_sysUser.objects.get(user_id=usercode)
    role_id = select_sysUser.objects.get(user_id__exact=usercode).role_id
    role_name = Select_Role.objects.get(id = role_id).role_name

    menu_list = Menu.objects.all()

    menu_list = menu_list.distinct()
    menu1 = menu_list.filter(menu_classify='学生').values()
    menu2 = menu_list.filter(menu_classify='教学管理员').values()
    menu3 = menu_list.filter(menu_classify='教学所长').values()
    menu4 = menu_list.filter(menu_classify='教师').values()



    if role_name == '学生':
        menus = [menu1]
        return menus
    elif role_name == '教学管理员':
        menus = [menu2]
        return menus
    elif role_name =='教学所长':
        menus = [menu3,menu4]
        return menus
    elif role_name =='教师':
        menus = [menu4]
        return menus

def error(req):
    if req.method == 'POST':
        return HttpResponseRedirect('/app/')
    return render_to_response('error.html')

def not_user(req):
    if req.method == 'POST':
        return HttpResponseRedirect('/app/')
    return render_to_response('not_user.html')

def password_wrong(req):
    if req.method == 'POST':
        return HttpResponseRedirect('/app/')
    return render_to_response('password_wrong.html')

def teacher_index(req):
    usercode = req.COOKIES.get('usercode', '')
    if usercode:
        return render_to_response('teacher_index.html',{'menus': get_menu(usercode)})
    else:
        return HttpResponseRedirect('/app/error/')

def supervisor_index(req):
    usercode = req.COOKIES.get('usercode', '')
    if usercode:
        return render_to_response('supervisor_index.html',{'menus': get_menu(usercode)})
    else:
        return HttpResponseRedirect('/app/error/')

def director_index(req):
    usercode = req.COOKIES.get('usercode', '')
    if usercode:
        return render_to_response('director_index.html',{'menus': get_menu(usercode)})
    else:
        return HttpResponseRedirect('/app/error/')


def login(req):
    if req.method == 'POST':
        form = LoginForm(req.POST)
        if form.is_valid():
            usercode = form.cleaned_data['user_code']
            USER = select_sysUser.objects.filter(user_id__exact=usercode)
            if not USER:
                return HttpResponseRedirect('/app/not_user/')

            user = select_sysUser.objects.filter(user_id__exact=usercode, password__exact=pc.encrypt(form.cleaned_data['password']))
            if not user:
                return HttpResponseRedirect('/app/password_wrong/')
            test = select_sysUser.objects.get(user_id__exact=usercode)



            role_id = test.role_id
            if user and role_id == 1:
                response = HttpResponseRedirect('/app/student_index/')
                response["P3P", "CP='IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT'"] = "P3P", "CP='IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT'"

                response.set_cookie('usercode', usercode, 36000)
                response.set_cookie('userid', user[0].user_id, 36000)
                print '2'
                return response
            elif user and role_id == 2:
                response = HttpResponseRedirect('/app/supervisor_index/')

                response.set_cookie('usercode', usercode, 36000)
                response.set_cookie('userid', user[0].user_id, 36000)

                return response
            elif user and role_id == 3:
                response = HttpResponseRedirect('/app/director_index/')

                response.set_cookie('usercode', usercode, 36000)
                response.set_cookie('userid', user[0].user_id, 36000)
                response.set_cookie('institution_id', user[0].institution_id, 36000)
                return response
            elif user and role_id == 4:
                response = HttpResponseRedirect('/app/teacher_index/')

                response.set_cookie('usercode', usercode, 36000)
                response.set_cookie('userid', user[0].user_id, 36000)


                return response
            else:
                return HttpResponseRedirect('/app/error/')

    else:
        form = LoginForm()

    ress = render_to_response('login.html', {'form': form})
    ress.delete_cookie('usercode')
    ress.delete_cookie('userid')

    return ress





##周文超，教办管理员  新增


def supervisor_teacherMessage(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_teacherMessage.html',{'menus': get_menu(usercode)})


def supervisor_studentMessage(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_studentMessage.html',{'menus': get_menu(usercode)})


def supervisor_Maintain(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_Maintain.html',{'menus': get_menu(usercode)})

def supervisor_teacherMessage(req):

    usercode = req.COOKIES.get('usercode', '')
    if req.method == "POST":
        uf = FileForm1(req.POST, req.FILES)
        if uf.is_valid():
            # get the info of the form
            name = uf.cleaned_data['name']

            DBoperater.supervisor_saveSelectFileTeacher(name)
    uf = FileForm1()
    return render_to_response('supervisor_teacherMessage.html', {'menus': get_menu(usercode), 'uf': uf})


def supervisor_studentMessage(req):

    usercode = req.COOKIES.get('usercode', '')
    if req.method == "POST":
        uf = FileForm1(req.POST, req.FILES)
        if uf.is_valid():
            # get the info of the form
            name = uf.cleaned_data['name']

            DBoperater.supervisor_saveSelectFileStudent(name)

    uf = FileForm1()
    return render_to_response('supervisor_studentMessage.html', {'menus': get_menu(usercode), 'uf': uf})

###周文超

##张煜，学生    新增


def student_index(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('student_index.html', {'menus': get_menu(usercode), 'id':id})
def student_chooseTopic(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('student_chooseTopic.html', {'menus': get_menu(usercode), 'id':id})
def student_checkTopic(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('student_checkTopic.html', {'menus': get_menu(usercode), 'id':id})
def student_download(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('student_download.html', {'menus': get_menu(usercode), 'id':id})
#张煜


### 韩佳琦 ， 教学所长   新增

def director_check(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('director_check.html',{'menus': get_menu(usercode)})

def director_manage(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('director_manage.html',{'menus': get_menu(usercode)})

def director_number(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('director_number.html',{'menus': get_menu(usercode)})

def director_manage(req):

    usercode = req.COOKIES.get('usercode', '')
    if req.method == "POST":
        uf = FileForm1(req.POST, req.FILES)
        if uf.is_valid():
            # get the info of the form
            name = uf.cleaned_data['name']

            DBoperater.director_uptopic(name)
    uf = FileForm1()
    return render_to_response('director_manage.html',{'menus': get_menu(usercode), 'uf': uf})







###   韩佳琦



### 许国斌 ， 教师  新增

def teacher_topic(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('teacher_topic.html',{'menus': get_menu(usercode)})

def teacher_chooseStudent(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('teacher_chooseStudent.html',{'menus': get_menu(usercode)})







#许国斌


# 王恩瑞  ，教学所长   新增

def supervisor_check(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_check.html',{'menus': get_menu(usercode)})


def supervisor_download(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_download.html',{'menus': get_menu(usercode)})

def supervisor_checkByTeacher(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_checkByTeacher.html',{'menus': get_menu(usercode)})

def supervisor_checkByStudent(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_checkByStudent.html',{'menus': get_menu(usercode)})

def supervisor_checkByTopic(req):

    usercode = req.COOKIES.get('usercode', '')
    return render_to_response('supervisor_checkByTopic.html',{'menus': get_menu(usercode)})

# 王恩瑞



if __name__ == "__main__":
    user = SysUser.objects.filter(user_id__exact=1, password__exact=1)
    print user
