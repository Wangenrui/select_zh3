# coding=utf-8

from django.http import HttpResponse, StreamingHttpResponse
from rest_framework import renderers
from password import prpcrypt
from models import SysUser, Role,select_sysUser,Application_state,File
from . import DBoperater, views
import os
import json
import datetime
from nortify import send_email_notification

pc = prpcrypt('boomboomboomboom')

def supervisor_get_date(req):
    dbresult = DBoperater.supervisor_getDate()
    return HttpResponse(json.dumps(dbresult[1]))


def director_get_alltopicnum(req):

    userid = req.COOKIES.get("userid", "")
    dbresult = DBoperater.director_getAlltopicnum(userid)
    return HttpResponse(json.dumps(dbresult[1]))


def director_get_dividedtopicnum(req):
    userid = req.COOKIES.get("userid", "")
    dbresult = DBoperater.director_getDividedtopicnum(userid)
    return HttpResponse(json.dumps(dbresult[1]))

def director_get_resttopicnum(req):
    userid = req.COOKIES.get("userid", "")
    dbresult = DBoperater.director_getResttopicnum(userid)
    return HttpResponse(json.dumps(dbresult[1]))

class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def changepassword(req):
    print '改密码'
    dict={}
    newpwd = req.GET.get("new_pwd", "")

    usr_code = req.COOKIES.get('usercode')
    print newpwd
    print usr_code
    user1 = select_sysUser.objects.get(user_id=usr_code)
    user1.password = pc.encrypt(newpwd)
    user1.save()
    dict['message'] = '密码修改成功！'
    print dict
    return HttpResponse(json.dumps(dict))


def get_provinceid(req):

    company_id = req.COOKIES.get('company_id', '')
    dbresult = DBoperater.getProvinceid(company_id)
    return HttpResponse(dbresult[1])



#周文超，教办管理员  新增

def supervisor_getuserinfo(req):
    dict = {}
    info = '数据获取成功'
    try:
        userid = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.supervisor_getUserInfo(userid)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def supervisor_get_year(req):
    dbresult = DBoperater.supervisor_getYear()
    return HttpResponse(json.dumps(dbresult[1]))


def supervisor_get_datebyid(req):

    id = req.GET.get('id', '')
    dbresult = DBoperater.supervisor_getDatebyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def supervisor_set_date(req):
    dict = {}
    info = ' Set date success'
    try:
        if req.method == 'POST':
            year = req.POST.get('year')
            av_start = req.POST.get('av_start', '')
            av_end = req.POST.get('av_end', '')
            write_sub_start = req.POST.get('write_sub_start', '')
            write_sub_end = req.POST.get('write_sub_end', '')
            stu_select_start= req.POST.get('stu_select_start', '')
            stu_select_end = req.POST.get('stu_select_end', '')
            tea_select_start = req.POST.get('tea_select_start', '')

            dbresult = DBoperater.supervisor_setDate(
                year = year      ,
                av_start = av_start ,
                av_end = av_end ,
                write_sub_start = write_sub_start        ,
                write_sub_end = write_sub_end,
                stu_select_start = stu_select_start,
                stu_select_end = stu_select_end,
                tea_select_start = tea_select_start
            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def supervisor_add_achieve_year(req):
    dict = {}
    info = 'Add add_achieve_year Success'
    try:
        if req.method == 'POST':
            achieve_year = req.POST.get('achieve_year', '')
            nextyear = req.POST.get('nextyear', '')

            dbresult = DBoperater.supervisor_addAchieveyear(
                nextyear           = nextyear,
                achieve_year       = achieve_year,
            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def supervisor_get_institution(req):
    dbresult = DBoperater.supervisor_getInstitution()
    return HttpResponse(json.dumps(dbresult[1]))


def supervisor_get_teacherbyid(req):
    id = req.GET.get('id', '')
    dbresult = DBoperater.supervisor_getTeacherbyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def supervisor_del_teacherbyid(req):
    dict = {}
    info = '数据删除成功'
    try:
        id = req.GET.get('id')
        dbresult = DBoperater.supervisor_delTeacherbyid(id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def supervisor_add_teachermessage(req):
    dict = {}
    info = 'Add teachermessage Success'
    try:
        if req.method == 'POST':
            teacher_name = req.POST.get('teacher_name', '')
            teacher_id = req.POST.get('teacher_id', '')
            sex_id = req.POST.get('sex_id', '')
            telephone = req.POST.get('telephone', '')
            institution_id = req.POST.get('institution_id', '')
            major_id = req.POST.get('major_id', '')

            dbresult = DBoperater.supervisor_addteacherMessage(

                teacher_name       =teacher_name,
                teacher_id        = teacher_id,
                sex_id        = sex_id ,
                telephone        = telephone        ,
                institution_id        = institution_id,
                major_id    =   major_id

            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def supervisor_update_teachermessage(req):
    dict = {}
    info = 'Update teachermessage success'
    try:
        if req.method == 'POST':
            id = req.POST.get('id')
            teacher_name = req.POST.get('teacher_name', '')
            teacher_id = req.POST.get('teacher_id', '')
            sex_id = req.POST.get('sex_id', '')
            telephone = req.POST.get('telephone', '')
            institution_id = req.POST.get('institution_id', '')
            major_id = req.POST.get('major_id', '')

            dbresult = DBoperater.supervisor_updateTeachermessage(
                id            = id                    ,
                teacher_name  = teacher_name            ,
                teacher_id    = teacher_id ,
                sex_id        = sex_id        ,
                telephone     = telephone        ,
                institution_id= institution_id  ,
                major_id      = major_id

            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))




def supervisor_get_selectteacher(req):

    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')
    dbresult = DBoperater.supervisor_getSelectteacher(limit, offset,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def supervisor_get_selectstudent(req):

    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')
    dbresult = DBoperater.supervisor_getSelectstudent(limit, offset,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def supervisor_get_studentbyid(req):

    id = req.GET.get('id', '')
    dbresult = DBoperater.supervisor_getStudentbyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def supervisor_del_studentbyid(req):

    dict = {}
    info = '数据删除成功'
    try:
        id = req.GET.get('id')
        dbresult = DBoperater.supervisor_delStudentbyid(id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def supervisor_add_studentmessage(req):
    dict = {}
    info = 'Add studentmessage Success'
    try:
        if req.method == 'POST':
            stu_name = req.POST.get('stu_name', '')
            sex_id = req.POST.get('sex_id', '')
            stu_id = req.POST.get('stu_id', '')
            stu_major_id = req.POST.get('stu_major_id', '')
            stu_class = req.POST.get('stu_class', '')
            stu_score = req.POST.get('stu_score', '')
            tel = req.POST.get('tel', '')


            dbresult = DBoperater.supervisor_addstudentMessage(

                stu_name       = stu_name,
                sex_id         = sex_id,
                stu_id         = stu_id ,
                stu_major_id   = stu_major_id,
                stu_class      = stu_class,
                stu_score      = stu_score,
                tel            = tel

            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))




def supervisor_update_studentmessage(req):
    dict = {}
    info = 'Update studentmessage success'
    try:
        if req.method == 'POST':
            id = req.POST.get('id')
            stu_name = req.POST.get('stu_name', '')
            sex_id = req.POST.get('sex_id', '')
            stu_id = req.POST.get('stu_id', '')
            stu_major_id = req.POST.get('stu_major_id', '')
            stu_class = req.POST.get('stu_class', '')
            stu_score = req.POST.get('stu_score','')
            tel= req.POST.get('tel', '')

            dbresult = DBoperater.supervisor_updateStudentmessage(
                id             = id      ,
                stu_name       = stu_name ,
                sex_id         = sex_id ,
                stu_id         = stu_id        ,
                stu_major_id   = stu_major_id,
                stu_class      = stu_class,
                stu_score          = stu_score,
                tel            = tel
            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def supervisor_initstudent(req):
    dict = {}
    info = 'Update supervisor_initstudent success'
    try:
        if req.method == 'POST':

            dbresult = DBoperater.supervisor_initStudent()

            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))




#周文超


#张煜，学生    新增


def download(req):
    filename = req.GET.get("filename", "")

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename.replace("upload/",""))
    response['Content-Length'] = os.path.getsize(filename)

    return response




def student_get_application(req):
    stu_no=req.COOKIES.get('userid','')
    dbresult = DBoperater.student_getApplication(stu_no)
    return HttpResponse(json.dumps(dbresult[1]))

def student_get_topic(req):
    stuMajor = req.GET.get('stuMajor', '')
    dbresult = DBoperater.student_getTopic(stuMajor)
    return HttpResponse(json.dumps(dbresult[1]))

def student_get_topic_introduction(req):
    topic_id = req.GET.get('topic_id', '')
    dbresult = DBoperater.student_getTopicIntroduction(topic_id)
    return HttpResponse(dbresult[1])

def student_get_file(req):
    limit = req.GET.get("limit", "")
    offset = req.GET.get("offset", "")
    stu_no = req.COOKIES.get('userid', '')
    state = Application_state.objects.get(selected_stu_no=stu_no)
    subject = state.topic
    dbresult = DBoperater.student_getFile(limit, offset,subject)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def student_add_application(req):
    dict = {}
    try:
        if req.method == 'POST':
            stu_no = req.POST.get('stu_no', '')
            id1 = req.POST.get('id1', '')
            volunteer_no1 = req.POST.get('volunteer_no1', '')
            volunteer_topic_no_id1= req.POST.get('volunteer_topic_no_id1', '')
            id2 = req.POST.get('id2', '')
            volunteer_no2 = req.POST.get('volunteer_no2', '')
            volunteer_topic_no_id2 = req.POST.get('volunteer_topic_no_id2', '')
            id3 = req.POST.get('id3', '')
            volunteer_no3 = req.POST.get('volunteer_no3', '')
            volunteer_topic_no_id3 = req.POST.get('volunteer_topic_no_id3', '')
            id4 = req.POST.get('id4', '')
            volunteer_no4 = req.POST.get('volunteer_no4', '')
            volunteer_topic_no_id4 = req.POST.get('volunteer_topic_no_id4', '')
            id5 = req.POST.get('id5', '')
            volunteer_no5 = req.POST.get('volunteer_no5', '')
            volunteer_topic_no_id5 = req.POST.get('volunteer_topic_no_id5', '')
            id6 = req.POST.get('id6', '')
            volunteer_no6 = req.POST.get('volunteer_no6', '')
            volunteer_topic_no_id6 = req.POST.get('volunteer_topic_no_id6', '')

            dbresult = DBoperater.student_addApplication(
                stu_no=stu_no,
                id1=id1,
                volunteer_no1=volunteer_no1,
                volunteer_topic_no_id1=volunteer_topic_no_id1,
                id2 = id2,
                volunteer_no2 = volunteer_no2,
                volunteer_topic_no_id2 = volunteer_topic_no_id2,
                id3 = id3,
                volunteer_no3 = volunteer_no3,
                volunteer_topic_no_id3 = volunteer_topic_no_id3,
                id4 = id4,
                volunteer_no4 = volunteer_no4,
                volunteer_topic_no_id4 = volunteer_topic_no_id4,
                id5 = id5,
                volunteer_no5 = volunteer_no5,
                volunteer_topic_no_id5 = volunteer_topic_no_id5,
                id6 = id6,
                volunteer_no6 = volunteer_no6,
                volunteer_topic_no_id6 = volunteer_topic_no_id6)
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def student_getstuinfo(req):
    dict = {}
    info = '数据获取成功'
    try:

        userid = req.COOKIES.get('userid', '')

        dbresult = DBoperater.student_getStuInfo(userid)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def student_getstate(req):
    dict = {}
    info = '数据获取成功'
    try:
        stu_no = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.student_getState(stu_no)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(renderers.JSONRenderer().render(dict))


def student_getdate(req):
    dict = {}
    info = '数据获取成功'
    try:
        stu_no = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.student_getDate(stu_no)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(renderers.JSONRenderer().render(dict))


#张煜




##韩佳琦 ， 教学所长     新增

def director_del_topic(req):

    dict = {}
    info = '数据删除成功'
    try:
        id = req.GET.get('id')
        dbresult = DBoperater.director_delTopic(id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_gettime(req):
    dict = {}
    info = '数据获取成功'
    try:
        tea_no = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.director_getTime(tea_no)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(renderers.JSONRenderer().render(dict))

def director_getstuinfo(req):
    dict = {}
    info = '数据获取成功'
    try:
        userid = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.director_getStuInfo(userid)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_get_insti(req):

    dbresult = DBoperater.director_getInsti()
    return HttpResponse(json.dumps(dbresult[1]))

def director_gettopic(req):
    institution_id = req.COOKIES.get('institution_id', '')
    province_id = req.GET.get("province_id", "")
    dbresult = DBoperater.director_getTopic(institution_id,province_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))


def director_getjianjie(req):
    institution_id = req.COOKIES.get('institution_id', '')
    topic_id = req.GET.get("topic", "")
    dbresult = DBoperater.director_getjianjie(institution_id,topic_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))
def director_getnum(req):

    tea_id = req.GET.get("teaid", "")
    dbresult = DBoperater.director_getnum(tea_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))
def director_getnum1(req):

    tea_id = req.GET.get("teaid", "")
    dbresult = DBoperater.director_getnum1(tea_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))




def director_get_class(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.director_getClass(institution_id)
    return HttpResponse(json.dumps(dbresult[1]))


def director_get_selectstudent(req):
    institution_id = req.COOKIES.get('institution_id', '')
    tea_no = req.GET.get("tea_no", "")
    class_id =req.GET.get("class_id","")
    stustu = req.GET.get("stustu", "")

    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')
    dbresult = DBoperater.director_getSelectstudent(institution_id,tea_no,class_id,stustu,limit, offset,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def director_getteacher(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.director_getTeacher(institution_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))


def director_get_teacc(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.director_getTeacc(institution_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))

def director_get_teach(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.director_getTeacc(institution_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))



def director_get_studentnobyid(req):

    id = req.GET.get('id', '')
    dbresult = DBoperater.director_getStudentnobyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def director_update_topic(req):
    dict = {}
    info = 'Update topic success'
    try:
        if req.method == 'POST':
            id = req.POST.get('id')

            stu_id = req.POST.get('stu_id', '')
            submit = req.POST.get('submit', '')
            topic_id = req.POST.get('topic_id', '')

            dbresult = DBoperater.director_updateTopic(
                id=id,
                stu_id=stu_id,
                topic_id=topic_id,
                submit=submit

            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_update_num(req):
    dict = {}
    info = 'Update num success'
    try:
        if req.method == 'POST':



            teacc = req.POST.get('teaccc', '')

            topic_num = req.POST.get('num2', '')


            dbresult = DBoperater.director_updateNum(

                teacc=teacc,
                topic_num=topic_num

            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_addtopic(req):
    dict = {}
    info = 'Add Topic Success'
    try:
        if req.method == 'POST':
            teacc = req.POST.get('teaccc', '')
            userid = req.COOKIES.get("userid", "")
            subject = req.POST.get('subject', '')
            introduction = req.POST.get('introduction', '')
            subject_property_id = req.POST.get('subject_property_id', '')
            other_introduction= req.POST.get('other_introduction', '')
            combine_actual = req.POST.get('combine_actual', '')
            company_name= req.POST.get('company_name', '')
            implementation_state= req.POST.get('implementation_state', '')
            english_title= req.POST.get('english_title', '')



            dbresult = DBoperater.director_Addintro(
                teacc=teacc,
                userid=userid,
                subject = subject,
                introduction = introduction,
                subject_property_id = subject_property_id,
                other_introduction = other_introduction,
                combine_actual= combine_actual,
                company_name = company_name,
                implementation_state = implementation_state,
                english_title = english_title,


            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_addtopicnum(req):
    dict = {}
    info = 'Add Topicnum Success'
    try:
        if req.method == 'POST':
            teacc = req.POST.get('teaccc', '')

            topic_num = req.POST.get('topic_num', '')



            dbresult = DBoperater.director_addtopicNum(
                teacc=teacc,
                topic_num = topic_num


            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_xiugaitopicnum(req):
    dict = {}
    info = 'Add Topicnum Success'
    try:
        if req.method == 'POST':

            teacc = req.POST.get('teaccc', '')

            topic_num = req.POST.get('topic_num', '')



            dbresult = DBoperater.director_xiugaitopicNum(

                teacc=teacc,
                topic_num = topic_num


            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def get_teatoopic(req):
    userid=req.COOKIES.get("userid", "")
    limit = req.GET.get("limit", "")
    offset = req.GET.get("offset", "")
    tea_no = req.GET.get("tea_no", "")
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')

    dbresult = DBoperater.getTeaToopic(limit, offset,tea_no,userid,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def director_xiugaitopic(req):
    dict = {}
    info = 'Add Equipment Success'
    try:
        if req.method == 'POST':
            id = req.POST.get('id', '')
            teacc = req.POST.get('teaccc', '')
            subject = req.POST.get('subject', '')
            introduction = req.POST.get('introduction', '')
            subject_property_id = req.POST.get('subject_property_id', '')
            other_introduction = req.POST.get('other_introduction', '')
            combine_actual = req.POST.get('combine_actual', '')
            company_name = req.POST.get('company_name', '')
            implementation_state = req.POST.get('implementation_state', '')
            english_title = req.POST.get('english_title', '')




            dbresult = DBoperater.xiugaiTopic(
                id=id,
                teacc=teacc,
                subject=subject,
                introduction=introduction,
                subject_property_id=subject_property_id,
                other_introduction=other_introduction,
                combine_actual=combine_actual,
                company_name=company_name,
                implementation_state=implementation_state,
                english_title=english_title,



            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def director_numberbyid(req):
    id = req.GET.get('id', '')

    dbresult = DBoperater.director_Numberbyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def get_teatoopicnum(req):

    institutionid = req.COOKIES.get("institution_id", "")
    majorid = req.GET.get("major", "")
    limit = req.GET.get("limit", "")
    offset = req.GET.get("offset", "")
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')



    dbresult = DBoperater.getTeaToopicnum(limit, offset,institutionid,majorid,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))
##韩佳琦


##许国斌 ， 教师    新增

def teacher_get_topicbyid(req):
    id = req.GET.get('id', '')
    dbresult = DBoperater.teacher_getTopicbyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def teacher_get_topicnumbyid(req):
    userid = req.COOKIES.get("userid", "")

    dbresult = DBoperater.teacher_getTopicnumbyid(userid)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def teacher_gettopicnum(req):
    userid = req.COOKIES.get("userid", "")

    dbresult = DBoperater.teacher_getTopicnum(userid)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))



def get_teafile(req):
    userid=req.COOKIES.get("userid", "")
    limit = req.GET.get("limit", "")
    offset = req.GET.get("offset", "")
    dbresult = DBoperater.getTeafile(userid,
         limit, offset)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def getteainfo(req):
    dict = {}
    info = '数据获取成功'
    try:
        userid = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.getTeaInfo(userid)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def get_teatopic(req):
    userid=req.COOKIES.get("userid", "")
    limit = req.GET.get("limit", "")
    offset = req.GET.get("offset", "")
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')
    dbresult = DBoperater.getTeaTopic(limit, offset,userid,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def get_teatopic1(req):
    userid=req.COOKIES.get("userid", "")
    limit = req.GET.get("limit", "")
    offset = req.GET.get("offset", "")
    search = req.GET.get("search", '')
    sort = req.GET.get("sort", '')
    order = req.GET.get("order", '')
    dbresult = DBoperater.getTeaTopic1(limit, offset,userid,search,sort,order)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def get_student1(req):
    subject_id=req.GET.get('subject_id','')
    dbresult = DBoperater.getStudent1(subject_id)
    print dbresult
    return HttpResponse(json.dumps(dbresult[1]))

def get_student2(req):
    subject_id=req.GET.get('subject_id','')
    dbresult = DBoperater.getStudent2(subject_id)
    return HttpResponse(json.dumps(dbresult[1]))

def get_student3(req):
    subject_id=req.GET.get('subject_id','')
    dbresult = DBoperater.getStudent3(subject_id)
    return HttpResponse(json.dumps(dbresult[1]))

def get_stuinfo(req):
    student=req.GET.get('student','')
    dbresult = DBoperater.getStuinfo(student)
    return HttpResponse(json.dumps(dbresult[1]))



def get_state(req):
    subject_id = req.GET.get('subject_id', '')
    dbresult = DBoperater.getState(subject_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))



def add_student(req):
    dict = {}
    try:
        print '111'
        if req.method == 'POST':
            id = req.POST.get('id', '')
            topic= req.POST.get('topic', '')
            selected_stu_no = req.POST.get('selected_stu_no', '')


            dbresult = DBoperater.addStudent(
                id=id,
                topic=topic,
                selected_stu_no=selected_stu_no
                )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def update_topic(req):
    dict = {}
    info = 'Add Equipment Success'
    try:
        if req.method == 'POST':
            id = req.POST.get('id', '')
            userid = req.COOKIES.get("userid", "")
            subject = req.POST.get('subject', '')
            introduction = req.POST.get('introduction', '')
            subject_property_id = req.POST.get('subject_property_id', '')
            other_introduction = req.POST.get('other_introduction', '')
            combine_actual = req.POST.get('combine_actual', '')
            company_name = req.POST.get('company_name', '')
            implementation_state = req.POST.get('implementation_state', '')
            english_title = req.POST.get('english_title', '')




            dbresult = DBoperater.updateTopic(
                id=id,
                userid=userid,
                subject=subject,
                introduction=introduction,
                subject_property_id=subject_property_id,
                other_introduction=other_introduction,
                combine_actual=combine_actual,
                company_name=company_name,
                implementation_state=implementation_state,
                english_title=english_title,



            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))



def get_teachertopics(req):
    usr_id = req.COOKIES.get('usercode')
    dbresult = DBoperater.getTeachertopics(usr_id)
    return HttpResponse(json.dumps(dbresult[1]))


def add_file(req):
    dict = {}
    try:
        if req.method == 'POST':

            subject_id= req.POST.get('subject_id', '')


            dbresult = DBoperater.addfile(

                subject_id=subject_id)

            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def add_topic(req):
    dict = {}
    info = 'Add Topic Success'
    try:
        if req.method == 'POST':
            userid = req.COOKIES.get("userid", "")
            subject = req.POST.get('subject', '')
            introduction = req.POST.get('introduction', '')
            subject_property_id = req.POST.get('subject_property_id', '')
            other_introduction= req.POST.get('other_introduction', '')
            combine_actual = req.POST.get('combine_actual', '')
            company_name= req.POST.get('company_name', '')
            implementation_state= req.POST.get('implementation_state', '')
            english_title= req.POST.get('english_title', '')



            dbresult = DBoperater.addTopic(
                userid=userid,
                subject = subject,
                introduction = introduction,
                subject_property_id = subject_property_id,
                other_introduction = other_introduction,
                combine_actual= combine_actual,
                company_name = company_name,
                implementation_state = implementation_state,
                english_title = english_title,


            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))



def teacher_getdate(req):
    dict = {}
    info = '数据获取成功'
    try:
        tea_no = req.COOKIES.get('usercode', '')
        dbresult = DBoperater.teacher_getDate(tea_no)
        if dbresult[0] == 0:
            info = dbresult[1]
        else:
            dict = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(renderers.JSONRenderer().render(dict))



##许国斌


##王恩瑞 ， 教办管理员   新增

def get_selectstulast(req):

    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    dbresult = DBoperater.getSelectstulast(limit, offset)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def get_downdata(req):
    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    search = req.GET.get("search", '')
    major_id = req.GET.get("major_id", "")
    class_id = req.GET.get("class_id", "")
    institution_id = req.GET.get("institution_id", "")
    teacher_id = req.GET.get("teacher_id", "")
    sort = req.GET.get("sort", "")
    order = req.GET.get("order", "")
    dbresult = DBoperater.getDowndata(limit, offset,search, major_id,class_id,institution_id, teacher_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def get_selectbystu(req):
    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    dbresult = DBoperater.getSelectbystu(limit, offset)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def get_selectbysub(req):

    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    dbresult = DBoperater.getSelectbysub(limit, offset)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


def get_selectbytea(req):

    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    dbresult = DBoperater.getSelectbytea(limit, offset)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def get_class(req):
    dbresult = DBoperater.getClass()
    return HttpResponse(json.dumps(dbresult[1]))

def download_report(req):
    filename = req.GET.get("filename", "")

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'

    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    response['Content-Length'] = os.path.getsize(filename)

    return response

def get_institution(req):
    dbresult = DBoperater.getInstitution()
    return HttpResponse(json.dumps(dbresult[1]))

def get_teacher(req):
    institution_id = req.GET.get("institution_id","")
    dbresult = DBoperater.getTeacher(institution_id)
    return HttpResponse(json.dumps(dbresult[1]))



##王恩瑞

#11.11 ltl
def director_getmajor(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.director_getMajor(institution_id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult[1]))

def get_student4(req):
    subject_id=req.GET.get('subject_id','')
    dbresult = DBoperater.getStudent4(subject_id)
    return HttpResponse(json.dumps(dbresult[1]))

def get_student5(req):
    subject_id=req.GET.get('subject_id','')
    dbresult = DBoperater.getStudent5(subject_id)
    return HttpResponse(json.dumps(dbresult[1]))

def get_student6(req):
    subject_id=req.GET.get('subject_id','')
    dbresult = DBoperater.getStudent6(subject_id)
    return HttpResponse(json.dumps(dbresult[1]))

##11.11 zwc
def supervisor_getmajor(req):
    dbresult = DBoperater.supervisor_getMajor()
    return HttpResponse(json.dumps(dbresult[1]))

##11.12 zwc
def supervisor_set_topicnum(req):
    dict = {}
    info = 'Set Topic num Success'
    try:
        if req.method == 'POST':
            institution_id = req.POST.get('institution_id', '')
            topic_min = req.POST.get('topic_min', '')

            dbresult = DBoperater.supervisor_setTopicnum(
                institution_id = institution_id,
                topic_min = topic_min
            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def supervisor_get_topicnum(req):
    limit = req.GET.get("limit", '')
    offset = req.GET.get("offset", '')
    search = req.GET.get("search", '')
    dbresult = DBoperater.supervisor_getTopicnum(limit, offset,search)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))


## 11.18 ltl

def director_get_minmax(req):
    institution_id = req.COOKIES.get('institution_id', '')

    dbresult = DBoperater.director_Get_minmax(institution_id)
    print dbresult
    return HttpResponse(json.dumps(dbresult[1]))

def director_get_topicnum(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.director_getTopicnum(institution_id)
    return HttpResponse(json.dumps(dbresult[1]))

def giveup1(req):
    dict = {}
    try:
        subject_id = req.GET.get("subject_id", '')

        dbresult = DBoperater.Giveup1(subject_id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def giveup2(req):
    dict = {}
    try:
        subject_id = req.GET.get("subject_id", '')

        dbresult = DBoperater.Giveup2(subject_id)
        info = dbresult[1]
        print info
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    print dict
    return HttpResponse(json.dumps(dict))


def giveup3(req):
    dict = {}
    try:
        subject_id = req.GET.get("subject_id", '')

        dbresult = DBoperater.Giveup3(subject_id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def giveup4(req):
    dict = {}
    try:
        subject_id = req.GET.get("subject_id", '')

        dbresult = DBoperater.Giveup4(subject_id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))


def giveup5(req):
    dict = {}
    try:
        subject_id = req.GET.get("subject_id", '')

        dbresult = DBoperater.Giveup5(subject_id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def giveup6(req):
    dict = {}
    try:
        subject_id = req.GET.get("subject_id", '')

        dbresult = DBoperater.Giveup6(subject_id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

##11.18 zwc
def super_get_topicnumbyid(req):
    id = req.GET.get('id', '')
    dbresult = DBoperater.supervisor_getTopicNumbyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

def super_update_topicnum(req):
    dict = {}
    info = 'Update super_update_topicnum success'
    try:
        if req.method == 'POST':
            id = req.POST.get('id', '')
            institution_id = req.POST.get('institution_id', '')
            topic_min = req.POST.get('topic_min', '')

            dbresult = DBoperater.supervisor_updateTopicNum(
                id = id,
                institution_id = institution_id,
                topic_min = topic_min
            )
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

## 11.18 wer
def student_addintroduction(req):
    dict = {}
    try:
        if req.method == 'POST':
            userid = req.COOKIES.get("userid", "")
            stu_introduction = req.POST.get('introduction', '')

            dbresult = DBoperater.student_addIntruduction(
                userid=userid,

                stu_introduction=stu_introduction,

            )
            print 'stu_introduction' + stu_introduction;

            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def student_getintroduction(req):
    stu_no = req.COOKIES.get('userid', '')
    dbresult = DBoperater.student_getIntroduction(stu_no)
    return HttpResponse(dbresult[1])


## 11.22 wer
def stu_submitapplication(req):
    dict = {}
    try:
        if req.method == 'POST':
            submit = req.POST.get('submit', '')
            id1 = req.POST.get('id1', '')
            id2 = req.POST.get('id2', '')
            id3 = req.POST.get('id3', '')
            id4 = req.POST.get('id4', '')
            id5 = req.POST.get('id5', '')
            id6 = req.POST.get('id6', '')


            dbresult = DBoperater.stu_SubmitApplication(
                submit=submit,
                id1=id1,
                id2 = id2,
                id3 = id3,
                id4 = id4,
                id5 = id5,
                id6 = id6)
            info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

##11.27 ltl
def teacher_submit_topic(req):
    dict={}
    try:
        print '000'
        userid = req.COOKIES.get("userid", "")
        dbresult = DBoperater.Teacher_submit_topic(
                userid)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

def teacher_whether_submit(req):
    dict={}
    try:
        print '111'
        userid = req.COOKIES.get("userid", "")
        dbresult = DBoperater.Teacher_whether_submit(
                userid)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))

##12.03 wer
def download_title(req):
    filename = req.GET.get("filename", "")

    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'

    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    response['Content-Length'] = os.path.getsize(filename)

    return response

#12.05 ltl
def director_get_topicbyid(req):
    id = req.GET.get('id', '')
    dbresult = DBoperater.director_getTopicbyid(id)
    return HttpResponse(renderers.JSONRenderer().render(dbresult))

##12.05 zwc
def supervisor_getthismajor(req):
    institution_id = req.GET.get('institution_id', '')
    dbresult = DBoperater.supervisor_getThisMajor(institution_id)
    return HttpResponse(json.dumps(dbresult[1]))

##12.06 ltl
def director_getthismajor(req):
    institution_id = req.COOKIES.get('institution_id', '')
    dbresult = DBoperater.supervisor_getThisMajor(institution_id)
    return HttpResponse(json.dumps(dbresult[1]))

def teacher_del_topic(req):

    dict = {}
    info = '数据删除成功'
    try:
        id = req.GET.get('id')
        dbresult = DBoperater.teacher_delTopic(id)
        info = dbresult[1]
    except:
        import sys
        info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    dict['message'] = info
    return HttpResponse(json.dumps(dict))