#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import random
from random import choice

LOCAL_DB = {
    'HOST': '127.0.0.1',
    'PORT': 3306,
    'USER': 'root',
    'PASSWORD': 'P1ssW0rd',
    'INSTANCE': 'select_zh1'}

local_conn = MySQLdb.connect(host=LOCAL_DB['HOST'], user=LOCAL_DB['USER'],
                             passwd=LOCAL_DB['PASSWORD'], port=LOCAL_DB['PORT'], charset='utf8')
local_cur = local_conn.cursor()
local_conn.select_db(LOCAL_DB['INSTANCE'])


def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
        ]


def fetch_local(sql, arg):
    local_cur.execute(sql, arg)       
    return dictfetchall(local_cur)
#33

def process():
    try:
        print 'start daily task'        
        start_date = startdate()
        print '教师选学生起点：' + str(start_date)
        start_time = timetypechange(start_date)
        print '教师选学生起点时间戳：' + str(start_time)
        achieve_year = achieveyear()
        #第一志愿被分配
        if time.time() >= (start_time+11.5*60*60.0) and time.time() < (start_time+12.5*60*60.0):
            #找到本志愿阶段其志愿被选到的所有教师
            sql = '''SELECT a.volunteer_topic_no_id,b.tea_no FROM app_application a 
                         LEFT JOIN app_topic b ON b.id = a.volunteer_topic_no_id            
                         WHERE volunteer_no = 1 AND volunteer_topic_no_id>=0 AND volunteer_topic_no_id NOT IN 
                         (SELECT topic FROM app_application_state) GROUP BY b.tea_no'''
            rss = fetch_local(sql, [])
            #遍历每一个老师
            for rs in rss:
                tea_no = rs['tea_no']
                print '教师工号：'+str(tea_no)
                list_selects = []
                #查找该老师本志愿阶段所有被选题目
                sql = '''SELECT a.volunteer_topic_no_id FROM app_application a
                             LEFT JOIN app_topic b ON b.id=a.volunteer_topic_no_id
                             WHERE a.volunteer_no=1 AND b.tea_no = '''+str(tea_no)+''' AND b.year='''+str(achieve_year)+''' 
                              AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                              AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                             GROUP BY a.volunteer_topic_no_id'''
                rsts = fetch_local(sql, [])
                for rst in rsts:
                    #选出选该题目的绩点最高的学生
                    volunteer_topic_no_id = rst['volunteer_topic_no_id']
                    list_temp = []
                    sql = '''SELECT stu_no,score FROM
                                 (SELECT stu_no,volunteer_topic_no_id,score FROM app_application a 
                                 LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no 
                                 WHERE volunteer_no = 1 AND volunteer_topic_no_id = '''+str(volunteer_topic_no_id)+''' 
                                 AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                 AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                 ORDER BY score DESC limit 10000000000) T1 
                                 GROUP BY volunteer_topic_no_id'''
                    rs_ss = fetch_local(sql, [])
                    score = rs_ss[0]['score']
                    stu_no = rs_ss[0]['stu_no']
                    list_temp.append(score)
                    list_temp.append(stu_no)
                    list_temp.append(volunteer_topic_no_id)
                    list_selects.append(list_temp)
                #按绩点高低排列下被选中学生
                list_selects.sort(reverse=True)
                print '按绩点高低排列下被选中学生'
                print list_selects
                for list_select in list_selects:
                    selected_stu_no = list_select[1]
                    volunteer_topic_id = list_select[2]
                    # 查询该老师是否有规定数的题目被选
                    sql = '''SELECT a.tea_no,a.topic_num,selected_num FROM app_teacher_topic_num a 
                                 LEFT JOIN (SELECT b.tea_no AS btea_no,b.id AS bid, COUNT(*) selected_num FROM app_application_state a
                                 LEFT JOIN app_topic b ON b.id=a.topic WHERE year = ''' + str(
                                 achieve_year) + ''' GROUP BY b.tea_no) T1
                                 ON T1.btea_no=a.tea_no WHERE a.tea_no =''' + str(
                                 tea_no) + ''' AND a.year =''' + str(achieve_year)
                    ras = fetch_local(sql, [])
                    if len(ras)==0:
                        topic_num = 0
                        selected_num = 0
                    else:
                       topic_num = ras[0]['topic_num']
                       selected_num = ras[0]['selected_num']
                    print '分配题目数：'+str(topic_num)

                    if selected_num is None:
                        selected_num = 0
                    print '被选题目数：'+str(selected_num)

                    if (int(topic_num) > int(selected_num)):
                        # end查询该题目所属老师是否有规定数的题目被选
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                        print sql
                        # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                        sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                            selected_stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_id)
                        fetch_local(sql, [])
            print '第1志愿被分配'
        #第二志愿被分配
        elif time.time() >= (start_time+12.5*60*60.0) and time.time() < (start_time+13.5*60*60.0):
            # 找到本志愿阶段其志愿被选到的所有教师
            sql = '''SELECT a.volunteer_topic_no_id,b.tea_no FROM app_application a 
                                     LEFT JOIN app_topic b ON b.id = a.volunteer_topic_no_id            
                                     WHERE volunteer_no = 2 AND volunteer_topic_no_id>=0 AND volunteer_topic_no_id NOT IN 
                                     (SELECT topic FROM app_application_state) GROUP BY b.tea_no'''
            rss = fetch_local(sql, [])
            # 遍历每一个老师
            for rs in rss:
                tea_no = rs['tea_no']
                print '教师工号：' + str(tea_no)
                list_selects = []
                # 查找该老师本志愿阶段所有被选题目
                sql = '''SELECT a.volunteer_topic_no_id FROM app_application a
                                         LEFT JOIN app_topic b ON b.id=a.volunteer_topic_no_id
                                         WHERE a.volunteer_no=2 AND b.tea_no = ''' + str(tea_no) + ''' AND b.year=''' + str(achieve_year) + '''
                                          AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                          AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                         GROUP BY a.volunteer_topic_no_id'''
                rsts = fetch_local(sql, [])
                for rst in rsts:
                    # 选出选该题目的绩点最高的学生
                    volunteer_topic_no_id = rst['volunteer_topic_no_id']
                    list_temp = []
                    sql = '''SELECT stu_no,score FROM
                                             (SELECT stu_no,volunteer_topic_no_id,score FROM app_application a 
                                             LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no 
                                             WHERE volunteer_no = 2 AND volunteer_topic_no_id = ''' + str(volunteer_topic_no_id) + '''
                                             AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                             AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state) 
                                             ORDER BY score DESC limit 10000000000) T1 
                                             GROUP BY volunteer_topic_no_id'''
                    rs_ss = fetch_local(sql, [])
                    score = rs_ss[0]['score']
                    stu_no = rs_ss[0]['stu_no']
                    list_temp.append(score)
                    list_temp.append(stu_no)
                    list_temp.append(volunteer_topic_no_id)
                    list_selects.append(list_temp)
                # 按绩点高低排列下被选中学生
                list_selects.sort(reverse=True)
                print '按绩点高低排列下被选中学生'
                print list_selects
                for list_select in list_selects:
                    selected_stu_no = list_select[1]
                    volunteer_topic_id = list_select[2]
                    # 查询该老师是否有规定数的题目被选
                    sql = '''SELECT a.tea_no,a.topic_num,selected_num FROM app_teacher_topic_num a 
                                             LEFT JOIN (SELECT b.tea_no AS btea_no,b.id AS bid, COUNT(*) selected_num FROM app_application_state a
                                             LEFT JOIN app_topic b ON b.id=a.topic WHERE year = ''' + str(
                        achieve_year) + ''' GROUP BY b.tea_no) T1
                                             ON T1.btea_no=a.tea_no WHERE a.tea_no =''' + str(
                        tea_no) + ''' AND a.year =''' + str(achieve_year)
                    ras = fetch_local(sql, [])
                    topic_num = ras[0]['topic_num']
                    print '分配题目数：' + str(topic_num)
                    selected_num = ras[0]['selected_num']
                    if selected_num is None:
                        selected_num = 0
                    print '被选题目数：' + str(selected_num)

                    if (int(topic_num) > int(selected_num)):
                        # end查询该题目所属老师是否有规定数的题目被选
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                        print sql
                        # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                        sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                            selected_stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_id)
                        fetch_local(sql, [])
            print '第2志愿被分配'
        # 第三志愿被分配
        elif time.time() >= (start_time+13.5*60*60.0) and time.time() < (start_time+14.5*60*60.0):
            # 找到本志愿阶段其志愿被选到的所有教师
            sql = '''SELECT a.volunteer_topic_no_id,b.tea_no FROM app_application a 
                                     LEFT JOIN app_topic b ON b.id = a.volunteer_topic_no_id            
                                     WHERE volunteer_no = 3 AND volunteer_topic_no_id>=0 AND volunteer_topic_no_id NOT IN 
                                     (SELECT topic FROM app_application_state) GROUP BY b.tea_no'''
            rss = fetch_local(sql, [])
            # 遍历每一个老师
            for rs in rss:
                tea_no = rs['tea_no']
                print '教师工号：' + str(tea_no)
                list_selects = []
                # 查找该老师本志愿阶段所有被选题目
                sql = '''SELECT a.volunteer_topic_no_id FROM app_application a
                                         LEFT JOIN app_topic b ON b.id=a.volunteer_topic_no_id
                                         WHERE a.volunteer_no=3 AND b.tea_no = ''' + str(
                    tea_no) + ''' AND b.year=''' + str(achieve_year) + '''
                     AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                     AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                         GROUP BY a.volunteer_topic_no_id'''
                rsts = fetch_local(sql, [])
                for rst in rsts:
                    # 选出选该题目的绩点最高的学生
                    volunteer_topic_no_id = rst['volunteer_topic_no_id']
                    list_temp = []
                    sql = '''SELECT stu_no,score FROM
                                             (SELECT stu_no,volunteer_topic_no_id,score FROM app_application a 
                                             LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no 
                                             WHERE volunteer_no = 3 AND volunteer_topic_no_id = ''' + str(volunteer_topic_no_id) + ''' 
                                             AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                             AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                             ORDER BY score DESC limit 10000000000) T1 
                                             GROUP BY volunteer_topic_no_id'''
                    rs_ss = fetch_local(sql, [])
                    score = rs_ss[0]['score']
                    stu_no = rs_ss[0]['stu_no']
                    list_temp.append(score)
                    list_temp.append(stu_no)
                    list_temp.append(volunteer_topic_no_id)
                    list_selects.append(list_temp)
                # 按绩点高低排列下被选中学生
                list_selects.sort(reverse=True)
                print '按绩点高低排列下被选中学生'
                print list_selects
                for list_select in list_selects:
                    selected_stu_no = list_select[1]
                    volunteer_topic_id = list_select[2]
                    # 查询该老师是否有规定数的题目被选
                    sql = '''SELECT a.tea_no,a.topic_num,selected_num FROM app_teacher_topic_num a 
                                             LEFT JOIN (SELECT b.tea_no AS btea_no,b.id AS bid, COUNT(*) selected_num FROM app_application_state a
                                             LEFT JOIN app_topic b ON b.id=a.topic WHERE year = ''' + str(
                        achieve_year) + ''' GROUP BY b.tea_no) T1
                                             ON T1.btea_no=a.tea_no WHERE a.tea_no =''' + str(
                        tea_no) + ''' AND a.year =''' + str(achieve_year)
                    ras = fetch_local(sql, [])
                    topic_num = ras[0]['topic_num']
                    print '分配题目数：' + str(topic_num)
                    selected_num = ras[0]['selected_num']
                    if selected_num is None:
                        selected_num = 0
                    print '被选题目数：' + str(selected_num)

                    if (int(topic_num) > int(selected_num)):
                        # end查询该题目所属老师是否有规定数的题目被选
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                        print sql
                        # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                        sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                            selected_stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_id)
                        fetch_local(sql, [])
            print '第3志愿被分配'
        # 第四志愿被分配
        elif time.time() >= (start_time+14.5*60*60.0) and time.time() < (start_time+15.5*60*60.0):
            # 找到本志愿阶段其志愿被选到的所有教师
            sql = '''SELECT a.volunteer_topic_no_id,b.tea_no FROM app_application a 
                                     LEFT JOIN app_topic b ON b.id = a.volunteer_topic_no_id            
                                     WHERE volunteer_no = 4 AND volunteer_topic_no_id>=0 AND volunteer_topic_no_id NOT IN 
                                     (SELECT topic FROM app_application_state) GROUP BY b.tea_no'''
            rss = fetch_local(sql, [])
            # 遍历每一个老师
            for rs in rss:
                tea_no = rs['tea_no']
                print '教师工号：' + str(tea_no)
                list_selects = []
                # 查找该老师本志愿阶段所有被选题目
                sql = '''SELECT a.volunteer_topic_no_id FROM app_application a
                                         LEFT JOIN app_topic b ON b.id=a.volunteer_topic_no_id
                                         WHERE a.volunteer_no=4 AND b.tea_no = ''' + str(
                    tea_no) + ''' AND b.year=''' + str(achieve_year) + '''
                     AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                     AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                         GROUP BY a.volunteer_topic_no_id'''
                rsts = fetch_local(sql, [])
                for rst in rsts:
                    # 选出选该题目的绩点最高的学生
                    volunteer_topic_no_id = rst['volunteer_topic_no_id']
                    list_temp = []
                    sql = '''SELECT stu_no,score FROM
                                             (SELECT stu_no,volunteer_topic_no_id,score FROM app_application a 
                                             LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no 
                                             WHERE volunteer_no = 4 AND volunteer_topic_no_id = ''' + str(volunteer_topic_no_id) + ''' 
                                             AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                             AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                             ORDER BY score DESC limit 10000000000) T1 
                                             GROUP BY volunteer_topic_no_id'''
                    rs_ss = fetch_local(sql, [])
                    score = rs_ss[0]['score']
                    stu_no = rs_ss[0]['stu_no']
                    list_temp.append(score)
                    list_temp.append(stu_no)
                    list_temp.append(volunteer_topic_no_id)
                    list_selects.append(list_temp)
                # 按绩点高低排列下被选中学生
                list_selects.sort(reverse=True)
                print '按绩点高低排列下被选中学生'
                print list_selects
                for list_select in list_selects:
                    selected_stu_no = list_select[1]
                    volunteer_topic_id = list_select[2]
                    # 查询该老师是否有规定数的题目被选
                    sql = '''SELECT a.tea_no,a.topic_num,selected_num FROM app_teacher_topic_num a 
                                             LEFT JOIN (SELECT b.tea_no AS btea_no,b.id AS bid, COUNT(*) selected_num FROM app_application_state a
                                             LEFT JOIN app_topic b ON b.id=a.topic WHERE year = ''' + str(
                        achieve_year) + ''' GROUP BY b.tea_no) T1
                                             ON T1.btea_no=a.tea_no WHERE a.tea_no =''' + str(
                        tea_no) + ''' AND a.year =''' + str(achieve_year)
                    ras = fetch_local(sql, [])
                    topic_num = ras[0]['topic_num']
                    print '分配题目数：' + str(topic_num)
                    selected_num = ras[0]['selected_num']
                    if selected_num is None:
                        selected_num = 0
                    print '被选题目数：' + str(selected_num)

                    if (int(topic_num) > int(selected_num)):
                        # end查询该题目所属老师是否有规定数的题目被选
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                        print sql
                        # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                        sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                            selected_stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_id)
                        fetch_local(sql, [])
            print '第4志愿被分配'
        # 第五志愿被分配
        elif time.time() >= (start_time+15.5*60*60.0) and time.time() < (start_time+16.5*60*60.0):
            # 找到本志愿阶段其志愿被选到的所有教师
            sql = '''SELECT a.volunteer_topic_no_id,b.tea_no FROM app_application a 
                                     LEFT JOIN app_topic b ON b.id = a.volunteer_topic_no_id            
                                     WHERE volunteer_no = 5 AND volunteer_topic_no_id>=0 AND volunteer_topic_no_id NOT IN 
                                     (SELECT topic FROM app_application_state) GROUP BY b.tea_no'''
            rss = fetch_local(sql, [])
            # 遍历每一个老师
            for rs in rss:
                tea_no = rs['tea_no']
                print '教师工号：' + str(tea_no)
                list_selects = []
                # 查找该老师本志愿阶段所有被选题目
                sql = '''SELECT a.volunteer_topic_no_id FROM app_application a
                                         LEFT JOIN app_topic b ON b.id=a.volunteer_topic_no_id
                                         WHERE a.volunteer_no=5 AND b.tea_no = ''' + str(
                    tea_no) + ''' AND b.year=''' + str(achieve_year) + '''
                     AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                     AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                         GROUP BY a.volunteer_topic_no_id'''
                rsts = fetch_local(sql, [])
                for rst in rsts:
                    # 选出选该题目的绩点最高的学生
                    volunteer_topic_no_id = rst['volunteer_topic_no_id']
                    list_temp = []
                    sql = '''SELECT stu_no,score FROM
                                             (SELECT stu_no,volunteer_topic_no_id,score FROM app_application a 
                                             LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no 
                                             WHERE volunteer_no = 5 AND volunteer_topic_no_id = ''' + str(volunteer_topic_no_id) + ''' 
                                             AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                             AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                             ORDER BY score DESC limit 10000000000) T1 
                                             GROUP BY volunteer_topic_no_id'''
                    rs_ss = fetch_local(sql, [])
                    score = rs_ss[0]['score']
                    stu_no = rs_ss[0]['stu_no']
                    list_temp.append(score)
                    list_temp.append(stu_no)
                    list_temp.append(volunteer_topic_no_id)
                    list_selects.append(list_temp)
                # 按绩点高低排列下被选中学生
                list_selects.sort(reverse=True)
                print '按绩点高低排列下被选中学生'
                print list_selects
                for list_select in list_selects:
                    selected_stu_no = list_select[1]
                    volunteer_topic_id = list_select[2]
                    # 查询该老师是否有规定数的题目被选
                    sql = '''SELECT a.tea_no,a.topic_num,selected_num FROM app_teacher_topic_num a 
                                             LEFT JOIN (SELECT b.tea_no AS btea_no,b.id AS bid, COUNT(*) selected_num FROM app_application_state a
                                             LEFT JOIN app_topic b ON b.id=a.topic WHERE year = ''' + str(
                        achieve_year) + ''' GROUP BY b.tea_no) T1
                                             ON T1.btea_no=a.tea_no WHERE a.tea_no =''' + str(
                        tea_no) + ''' AND a.year =''' + str(achieve_year)
                    ras = fetch_local(sql, [])
                    topic_num = ras[0]['topic_num']
                    print '分配题目数：' + str(topic_num)
                    selected_num = ras[0]['selected_num']
                    if selected_num is None:
                        selected_num = 0
                    print '被选题目数：' + str(selected_num)

                    if (int(topic_num) > int(selected_num)):
                        # end查询该题目所属老师是否有规定数的题目被选
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                        print sql
                        # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                        sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                            selected_stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_id)
                        fetch_local(sql, [])
            print '第5志愿被分配'
        # 第六志愿被分配
        elif time.time() >= (start_time+16.5*60*60.0) and time.time() < (start_time+17.0*60*60.0):
            # 找到本志愿阶段其志愿被选到的所有教师
            sql = '''SELECT a.volunteer_topic_no_id,b.tea_no FROM app_application a 
                                     LEFT JOIN app_topic b ON b.id = a.volunteer_topic_no_id            
                                     WHERE volunteer_no = 6 AND volunteer_topic_no_id>=0 AND volunteer_topic_no_id NOT IN 
                                     (SELECT topic FROM app_application_state) GROUP BY b.tea_no'''
            rss = fetch_local(sql, [])
            # 遍历每一个老师
            for rs in rss:
                tea_no = rs['tea_no']
                print '教师工号：' + str(tea_no)
                list_selects = []
                # 查找该老师本志愿阶段所有被选题目
                sql = '''SELECT a.volunteer_topic_no_id FROM app_application a
                                         LEFT JOIN app_topic b ON b.id=a.volunteer_topic_no_id
                                         WHERE a.volunteer_no=6 AND b.tea_no = ''' + str(
                    tea_no) + ''' AND b.year=''' + str(achieve_year) + '''
                     AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                     AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                         GROUP BY a.volunteer_topic_no_id'''
                rsts = fetch_local(sql, [])
                for rst in rsts:
                    # 选出选该题目的绩点最高的学生
                    volunteer_topic_no_id = rst['volunteer_topic_no_id']
                    list_temp = []
                    sql = '''SELECT stu_no,score FROM
                                             (SELECT stu_no,volunteer_topic_no_id,score FROM app_application a 
                                             LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no 
                                             WHERE volunteer_no = 6 AND volunteer_topic_no_id = ''' + str(volunteer_topic_no_id) + ''' 
                                             AND volunteer_topic_no_id NOT IN (SELECT topic FROM app_application_state)
                                             AND a.stu_no NOT IN (SELECT selected_stu_no FROM app_application_state)
                                             ORDER BY score DESC limit 10000000000) T1 
                                             GROUP BY volunteer_topic_no_id'''
                    rs_ss = fetch_local(sql, [])
                    score = rs_ss[0]['score']
                    stu_no = rs_ss[0]['stu_no']
                    list_temp.append(score)
                    list_temp.append(stu_no)
                    list_temp.append(volunteer_topic_no_id)
                    list_selects.append(list_temp)
                # 按绩点高低排列下被选中学生
                list_selects.sort(reverse=True)
                print '按绩点高低排列下被选中学生'
                print list_selects
                for list_select in list_selects:
                    selected_stu_no = list_select[1]
                    volunteer_topic_id = list_select[2]
                    # 查询该老师是否有规定数的题目被选
                    sql = '''SELECT a.tea_no,a.topic_num,selected_num FROM app_teacher_topic_num a 
                                             LEFT JOIN (SELECT b.tea_no AS btea_no,b.id AS bid, COUNT(*) selected_num FROM app_application_state a
                                             LEFT JOIN app_topic b ON b.id=a.topic WHERE year = ''' + str(
                        achieve_year) + ''' GROUP BY b.tea_no) T1
                                             ON T1.btea_no=a.tea_no WHERE a.tea_no =''' + str(
                        tea_no) + ''' AND a.year =''' + str(achieve_year)
                    ras = fetch_local(sql, [])
                    topic_num = ras[0]['topic_num']
                    print '分配题目数：' + str(topic_num)
                    selected_num = ras[0]['selected_num']
                    if selected_num is None:
                        selected_num = 0
                    print '被选题目数：' + str(selected_num)

                    if (int(topic_num) > int(selected_num)):
                        # end查询该题目所属老师是否有规定数的题目被选
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                        print sql
                        # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                        sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                            selected_stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_id)
                        fetch_local(sql, [])
            print '第6志愿被分配'
        #自由分配start
        elif time.time() >= (start_time+17.0*60*60.0) and time.time() < (start_time+17.5*60*60.0):
            # 自由分配start
            sql = 'SELECT id  FROM app_major'''
            rs_majors = fetch_local(sql, [])
            for rs_major in rs_majors:
                listunstu = []
                listuntopics = []
                major_id = rs_major['id']
                print '专业id**************************************'
                print major_id
                # list of unselected student未选成功学生池
                sql = '''SELECT user_id FROM app_select_sysuser WHERE role_id=1 AND user_id NOT IN 
                                (SELECT selected_stu_no FROM app_application_state) 
                                AND major_id=''' + str(major_id) + ''' AND achieve_year=''' + str(achieve_year)
                rs_stus = fetch_local(sql, [])

                for rs_stu in rs_stus:
                    listunstu.append(rs_stu['user_id'])
                #题目池
                #先把老师的分配题目数查询到
                sql = '''SELECT tea_no FROM app_topic WHERE major_id =''' + str(major_id) + '''
                                AND year = '''+ str(achieve_year)+''' GROUP BY tea_no'''
                rs_teas = fetch_local(sql, [])
                for rs_tea in rs_teas:
                    tea_no = rs_tea['tea_no']
                    print tea_no
                    #每个老师分配题目数
                    sql = '''SELECT topic_num FROM  app_teacher_topic_num WHERE tea_no = '''+ str(tea_no)+''' AND year = '''+ str(achieve_year)
                    rs_tea_topics = fetch_local(sql, [])
                    if len(rs_tea_topics)==0:
                        topic_num = 0
                    else:
                        topic_num = rs_tea_topics[0]['topic_num']
                    #查询每个老师被选题目数
                    sql = '''SELECT COUNT(*) selected_num FROM app_application_state a 
                             LEFT JOIN app_topic b ON b.id=a.topic 
                             WHERE tea_no = ''' + str(tea_no) + ''' AND year=''' + str(achieve_year) + ''' GROUP BY b.tea_no '''
                    rs_tea_numeds = fetch_local(sql, [])
                    if len(rs_tea_numeds)==0:
                        selected_num = 0
                    else :
                        selected_num = rs_tea_numeds[0]['selected_num']
                    print '老师被选题目数'
                    print selected_num
                    #查询每个老师剩余本专业题目数
                    sql = '''SELECT COUNT(*) num FROM app_topic
                             WHERE tea_no = ''' + str(tea_no) + ''' AND year =''' + str(achieve_year) + ''' AND major_id=''' + str(major_id) + '''  
                             AND id NOT IN(SELECT topic FROM app_application_state) GROUP BY tea_no'''

                    rs_tea_num_lave = fetch_local(sql, [])
                    if len(rs_tea_num_lave)==0:
                        num_lave = 0
                    else :
                        num_lave = rs_tea_num_lave[0]['num']
                    print '老师剩余本专业题目数'
                    print num_lave
                    # 查询每个老师剩余本专业题目list
                    teatopiclist = []
                    sql = '''SELECT id FROM app_topic 
                             WHERE tea_no = ''' + str(tea_no) + ''' AND year =''' + str(achieve_year) + ''' 
                             AND major_id=''' + str(major_id) + ''' AND id NOT IN(SELECT topic FROM app_application_state) '''

                    rs_tea_topics = fetch_local(sql, [])
                    if len(rs_tea_topics)==0:
                        continue
                    for rs_tea_topic in rs_tea_topics:
                        teatopiclist.append(rs_tea_topic['id'])
                    lentlist = len(teatopiclist)
                    # 该老师需要进入本专业题目池的题目个数
                    num_sub = int(topic_num) - int(selected_num)
                    if(num_sub<=0):
                        continue
                    print '该老师需要进入本专业题目池的题目个数'
                    print num_sub
                    #从每个老师剩余本专业题目list中选出放进题目池中的题目
                    templist = []
                    if 0<lentlist<num_sub:
                        templist = random.sample(teatopiclist, lentlist)
                    elif lentlist>=num_sub:
                        templist = random.sample(teatopiclist, num_sub)
                    for temp in templist:
                        listuntopics.append(temp)

                print '学生池'
                print '人数' + str(len(listunstu))
                print listunstu
                random.shuffle(listuntopics)
                print '题目池'
                print '题目数' + str(len(listuntopics))
                print listuntopics
                #然后匹配
                if(len(listunstu)>len(listuntopics)):
                    print '该专业题目池中题目数小于学生池中学生数'
                    for i in range(len(listuntopics)):
                        selected_stu_no = listunstu[i]
                        volunteer_topic_no_id = listuntopics[i]
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_no_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])
                if (len(listuntopics) >= len(listunstu)):
                    print '该专业题目池中题目数大于等于学生池中学生数'
                    for i in range(len(listunstu)):
                        selected_stu_no = listunstu[i]
                        volunteer_topic_no_id = listuntopics[i]
                        sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                            volunteer_topic_no_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                        fetch_local(sql, [])

            print 'f'
        #自由分配结束
        else:
            print '未开始选学生或自由分配已结束'

        local_conn.commit()
        print 'end daily task'

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def startdate():
    try:
        sql = '''SELECT `select3_start` FROM `app_date_setting` WHERE `activation` =1'''
        rss = fetch_local(sql, [])
        start_date = rss[0]['select3_start']
        return start_date
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def timetypechange(sdate):
    #将其转换为时间数组
    timeArray = time.strptime(sdate, "%Y-%m-%d")
    #转换为时间戳:
    timeStamp = time.mktime(timeArray)
    return timeStamp

def achieveyear():
    try:
        sql = '''SELECT `year` FROM `app_date_setting` WHERE `activation` =1'''
        rss = fetch_local(sql, [])
        achieve_year = rss[0]['year']
        return achieve_year
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

print '*******************************************************************************************'
print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
process()

local_conn.commit()
local_cur.close()
local_conn.close()

exit()

