# coding=utf-8

from django.conf.urls import url, include
from . import views, datatrans, mobile, report
from django.contrib import admin

urlpatterns = (
    url(r'^$', views.login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^changepassword$', datatrans.changepassword, name='changepassword'),
    url(r'^getprovinceid', datatrans.get_provinceid, name='getprovince_id'),


    url(r'^error/$', views.error, name='error'),




    url(r'^report$', report.report, name='report'),

    url(r'^supervisor_get_date$', datatrans.supervisor_get_date, name='supervisor_get_date'),
    url(r'^director_get_alltopicnum', datatrans.director_get_alltopicnum, name='director_get_alltopicnum'),
    url(r'^director_get_dividedtopicnum', datatrans.director_get_dividedtopicnum, name='director_get_dividedtopicnum'),
    #周文超，教办管理员  新增
    url(r'^supervisor_index/$', views.supervisor_index, name='supervisor_index'),
    url(r'^supervisor_get_selectteacher$', datatrans.supervisor_get_selectteacher, name='supervisor_get_selectteacher'),
    url(r'^supervisor_get_selectstudent$', datatrans.supervisor_get_selectstudent, name='supervisor_get_selectstudent'),
    url(r'supervisor_teacherMessage/$', views.supervisor_teacherMessage, name='supervisor_teacherMessage'),
    url(r'supervisor_studentMessage/$', views.supervisor_studentMessage, name='supervisor_studentMessage'),
    url(r'supervisor_Maintain/$', views.supervisor_Maintain, name='supervisor_Maintain'),
    url(r'^supervisor_getYear$', datatrans.supervisor_get_year, name='supervisor_getYear'),


    url(r'^supervisor_add_teachermessage$', datatrans.supervisor_add_teachermessage, name='supervisor_add_teachermessage'),
    url(r'^supervisor_get_teacherbyid$', datatrans.supervisor_get_teacherbyid, name='supervisor_get_teacherbyid'),
    url(r'^supervisor_update_teachermessage$', datatrans.supervisor_update_teachermessage, name='supervisor_update_teachermessage'),
    url(r'^supervisor_del_teacherbyid$', datatrans.supervisor_del_teacherbyid, name='supervisor_del_teacherbyid'),

    url(r'^supervisor_getinstitution$', datatrans.supervisor_get_institution, name='supervisor_getinstitution'),
    url(r'^supervisor_add_studentmessage$', datatrans.supervisor_add_studentmessage, name='supervisor_add_studentmessage'),
    url(r'^supervisor_get_studentbyid$', datatrans.supervisor_get_studentbyid, name='supervisor_get_studentbyid'),
    url(r'^supervisor_update_studentmessage$', datatrans.supervisor_update_studentmessage, name='supervisor_update_studentmessage'),
    url(r'^supervisor_del_studentbyid$', datatrans.supervisor_del_studentbyid, name='supervisor_del_studentbyid'),

    url(r'^supervisor_get_datebyid$', datatrans.supervisor_get_datebyid, name='supervisor_get_datebyid'),
    url(r'^supervisor_set_date$', datatrans.supervisor_set_date, name='supervisor_set_date'),


    url(r'^supervisor_add_achieve_year$', datatrans.supervisor_add_achieve_year, name='supervisor_add_achieve_year'),
    url(r'^supervisor_getuserinfo$', datatrans.supervisor_getuserinfo, name='supervisor_getuserinfo'),
    url(r'^supervisor_init_student', datatrans.supervisor_initstudent, name='supervisor_init_student'),


    ##周文超


    #张煜，学生    新增

    url(r'^student_index/$', views.student_index, name='student_index'),
    url(r'student_chooseTopic/$', views.student_chooseTopic, name='student_chooseTopic'),
    url(r'student_checkTopic/$', views.student_checkTopic, name='student_checkTopic'),
    url(r'student_download/$', views.student_download, name='student_download'),

    url(r'^student_get_application', datatrans.student_get_application, name='student_get_application'),
    url(r'^student_get_topic$', datatrans.student_get_topic, name='student_get_topic'),
    url(r'^student_get_topic_introduction', datatrans.student_get_topic_introduction,
        name='student_get_topic_introduction'),
    url(r'^student_get_file', datatrans.student_get_file, name='student_get_file'),
    url(r'^student_addapplication', datatrans.student_add_application, name='student_addapplication'),

    url(r'^student_getstuinfo$', datatrans.student_getstuinfo, name='student_getstuinfo'),
    url(r'^student_getstate$', datatrans.student_getstate, name='student_getstate'),
    url(r'^student_getdate$', datatrans.student_getdate, name='student_getdate'),
    url(r'^download$', datatrans.download, name='download'),




    #张煜


    ##韩佳琦，教学所长    新增

    url(r'^director_index/$', views.director_index, name='director_index'),
    url(r'director_check/$',views.director_check,name='director_check'),
    url(r'^director_manage/$', views.director_manage, name='director_manage'),
    url(r'^director_number/$', views.director_number, name='director_number'),
    url(r'^director_get_selectstudent$', datatrans.director_get_selectstudent, name='director_get_selectstudent'),
    url(r'^director_getinsti', datatrans.director_get_insti, name='director_getinsti'),

    url(r'^director_getteacc', datatrans.director_get_teacc, name='director_getteacc'),
    url(r'^director_getteacher', datatrans.director_getteacher, name='director_getteacher'),
    url(r'^director_gettopic', datatrans.director_gettopic, name='director_gettopic'),
    url(r'^director_getclass', datatrans.director_get_class, name='director_getclass'),

    url(r'^director_get_studentnobyid', datatrans.director_get_studentnobyid, name='director_get_studentnobyid'),
    url(r'^director_update_topic', datatrans.director_update_topic, name='director_update_topic'),
    url(r'^director_update_num', datatrans.director_update_num, name='director_update_num'),

    url(r'^director_getstuinfo$', datatrans.director_getstuinfo, name='director_getstuinfo'),

    url(r'^director_gettime$', datatrans.director_gettime, name='director_gettime'),


    url(r'^director_getjianjie$', datatrans.director_getjianjie, name='director_getjianjie'),
    url(r'^director_getnum$', datatrans.director_getnum, name='director_getnum'),
    url(r'^director_getnum1$', datatrans.director_getnum1, name='director_getnum1'),
    url(r'^director_addtopic$', datatrans.director_addtopic, name='director_addtopic'),
url(r'^director_addtopicnum$', datatrans.director_addtopicnum, name='director_addtopicnum'),
    url(r'^get_teatoopic$', datatrans.get_teatoopic, name='get_teatoopic'),
url(r'^get_teatoopicnum$', datatrans.get_teatoopicnum, name='get_teatoopicnum'),
    url(r'^director_getteach', datatrans.director_get_teach, name='director_getteach'),
    url(r'^director_xiugaitopic$', datatrans.director_xiugaitopic, name='director_xiugaitopic'),
url(r'^director_xiugaitopicnum$', datatrans.director_xiugaitopicnum, name='director_xiugaitopicnum'),
    url(r'^director_del_topic', datatrans.director_del_topic, name='director_del_topic'),
url(r'^director_numberbyid$', datatrans.director_numberbyid, name='director_numberbyid'),

    ##韩佳琦


    ##许国斌 ， 教师    新增


    url(r'^teacher_index/$', views.teacher_index, name='teacher_index'),
    url(r'^teacher_topic/$', views.teacher_topic, name='teacher_topic'),
    url(r'^teacher_chooseStudent/$', views.teacher_chooseStudent, name='teacher_chooseStudent'),
    url(r'^update_topic', datatrans.update_topic, name='update_topic'),
    url(r'^add_topic', datatrans.add_topic, name='add_topic'),
    url(r'^getteainfo$', datatrans.getteainfo, name='getteainfo'),
    url(r'^get_student1$', datatrans.get_student1, name='get_student1'),
    url(r'^get_student2$', datatrans.get_student2, name='get_student2'),
    url(r'^get_student3$', datatrans.get_student3, name='get_student3'),
    url(r'^get_stuinfo$', datatrans.get_stuinfo, name='get_stuinfo'),
    url(r'^get_state', datatrans.get_state, name='get_state'),
    url(r'^get_teatopic$', datatrans.get_teatopic, name='get_teatopic'),
    url(r'^get_teatopic1$', datatrans.get_teatopic1, name='get_teatopic1'),
    url(r'^add_student', datatrans.add_student, name='add_student'),
    url(r'^get_teachertopics', datatrans.get_teachertopics, name='get_teachertopics'),

    url(r'^get_teafile$', datatrans.get_teafile, name='get_teafile'),
    url(r'^teacher_getdate$', datatrans.teacher_getdate, name='teacher_getdate'),
    url(r'^teacher_get_topicbyid$', datatrans.teacher_get_topicbyid, name='teacher_get_topicbyid'),
    url(r'^teacher_get_topicnumbyid', datatrans.teacher_get_topicnumbyid, name='teacher_get_topicnumbyid'),
    url(r'^teacher_gettopicnum', datatrans.teacher_gettopicnum, name='teacher_gettopicnum'),



    ##许国斌


    ##王恩瑞 ， 教办管理员  新增





    ##


    url(r'supervisor_checkByTeacher/$', views.supervisor_checkByTeacher, name='supervisor_checkByTeacher'),
    url(r'supervisor_checkByStudent/$', views.supervisor_checkByStudent, name='supervisor_checkByStudent'),
    url(r'supervisor_checkByTopic/$', views.supervisor_checkByTopic, name='supervisor_checkByTopic'),
    url(r'supervisor_download/$', views.supervisor_download, name='supervisor_download'),

    url(r'^report$', report.report, name='report'),
    url(r'^double_report$', report.double_report, name='double_report'),
    url(r'^download_report$', datatrans.download_report, name='download_report'),

    url(r'^get_institution', datatrans.get_institution, name='get_institution'),
    url(r'^get_teacher$', datatrans.get_teacher, name='get_teacher'),
    url(r'^get_class$', datatrans.get_class, name='get_class'),

    url(r'^get_selectbytea', datatrans.get_selectbytea, name='get_selectbytea'),
    url(r'^get_selectbysub', datatrans.get_selectbysub, name='get_selectbysub'),
    url(r'^get_selectbystu', datatrans.get_selectbystu, name='get_selectbystu'),
    url(r'^get_downdata', datatrans.get_downdata, name='get_downdata'),
    url(r'^get_selectstulast$', datatrans.get_selectstulast, name='get_selectstulast'),
    ##王恩瑞


    ##11.11 ltl
    url(r'^director_getmajor', datatrans.director_getmajor, name='director_getmajor'),
    url(r'^get_student4$', datatrans.get_student4, name='get_student4'),
    url(r'^get_student5$', datatrans.get_student5, name='get_student5'),
    url(r'^get_student6$', datatrans.get_student6, name='get_student6'),

    ##11.11 zwc
    url(r'^supervisor_getmajor', datatrans.supervisor_getmajor, name='supervisor_getmajor'),

    ##11.12 zwc
    url(r'^supervisor_set_topicnum', datatrans.supervisor_set_topicnum, name='supervisor_set_topicnum'),
    url(r'^supervisor_get_topicnum', datatrans.supervisor_get_topicnum, name='supervisor_get_topicnum'),

    ##11.18 ltl
    url(r'^director_get_minmax', datatrans.director_get_minmax, name='director_get_minmax'),
    url(r'^director_get_topicnum', datatrans.director_get_topicnum, name='director_get_topicnum'),
    url(r'^giveup1', datatrans.giveup1, name='giveup1'),
    url(r'^giveup2', datatrans.giveup2, name='giveup2'),
    url(r'^giveup3', datatrans.giveup3, name='giveup3'),
    url(r'^giveup4', datatrans.giveup4, name='giveup4'),
    url(r'^giveup5', datatrans.giveup5, name='giveup5'),
    url(r'^giveup6', datatrans.giveup6, name='giveup6'),

    ##11.18 zwc
    url(r'^super_get_topicnumbyid', datatrans.super_get_topicnumbyid, name='super_get_topicnumbyid'),
    url(r'^super_update_topicnum', datatrans.super_update_topicnum, name='super_update_topicnum'),

    ##11.18 wer
    url(r'^student_addintroduction', datatrans.student_addintroduction, name='student_addintroduction'),
    url(r'^student_getintroduction', datatrans.student_getintroduction, name='student_getintroduction'),

    ##11.22 wer
    url(r'^stu_submitapplication', datatrans.stu_submitapplication, name='stu_submitapplication'),


    ##11.27 ltl
    url(r'^teacher_submit_topic', datatrans.teacher_submit_topic, name='teacher_submit_topic'),
    url(r'^teacher_whether_submit', datatrans.teacher_whether_submit, name='teacher_whether_submit'),

    ##12.03 wer
    url(r'^download_title$', datatrans.download_title, name='download_title'),
    url(r'^summary_title$', report.summary_title, name='summary_title'),

    ##12.05 ltl
    url(r'^director_get_topicbyid', datatrans.director_get_topicbyid, name='director_get_topicbyid'),

    ##12.05 zwc
    url(r'^supervisor_getthismajor', datatrans.supervisor_getthismajor, name='supervisor_getthismajor'),

    url(r'^not_user/$', views.not_user, name='not_user'),
    url(r'^password_wrong/$', views.password_wrong, name='password_wrong'),
    url(r'^teacher_del_topic', datatrans.teacher_del_topic, name='teacher_del_topic'),


)
