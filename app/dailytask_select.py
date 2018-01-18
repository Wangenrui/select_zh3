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
    'PASSWORD': '1',
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
        start_time = timetypechange(start_date)
        #第一志愿被分配
        if time.time() >= start_time and time.time() < (start_time+24*60*60.0):

            sql = '''SELECT stu_no,volunteer_topic_no_id,MAX(score) FROM app_application a LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no WHERE volunteer_no = 1 AND volunteer_topic_no_id>=0 GROUP  BY volunteer_topic_no_id '''
            rss = fetch_local(sql, [])
            for rs in rss:
                stu_no = rs['stu_no']
                volunteer_topic_no_id = rs['volunteer_topic_no_id']
                sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES ('''+str(volunteer_topic_no_id)+','+str(stu_no)+','+str(1) +')'
                fetch_local(sql, [])
                # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                sql = '''DELETE FROM app_application WHERE  stu_no=''' +str(stu_no) +' OR volunteer_topic_no_id='+str(volunteer_topic_no_id)
                print sql
                fetch_local(sql, [])
        #第二志愿被分配
        elif time.time() >= (start_time+24*60*60.0) and time.time() < (start_time+2*24*60*60.0):
            sql = '''SELECT stu_no,volunteer_topic_no_id,MAX(score) FROM app_application a LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no WHERE volunteer_no = 2 AND volunteer_topic_no_id>=0 GROUP  BY volunteer_topic_no_id '''
            rss = fetch_local(sql, [])
            for rs in rss:
                stu_no = rs['stu_no']
                volunteer_topic_no_id = rs['volunteer_topic_no_id']
                sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                    volunteer_topic_no_id) + ',' + str(stu_no) + ',' + str(1) + ')'
                fetch_local(sql, [])
                # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                    stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_no_id)
                print sql
                fetch_local(sql, [])
        # 第三志愿被分配
        elif time.time() >= (start_time+2*24*60*60.0) and time.time() < (start_time+3*24*60*60.0):
            sql = '''SELECT stu_no,volunteer_topic_no_id,MAX(score) FROM app_application a LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no WHERE volunteer_no = 3 AND volunteer_topic_no_id>=0 GROUP  BY volunteer_topic_no_id '''
            rss = fetch_local(sql, [])
            for rs in rss:
                stu_no = rs['stu_no']
                volunteer_topic_no_id = rs['volunteer_topic_no_id']
                sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                    volunteer_topic_no_id) + ',' + str(stu_no) + ',' + str(1) + ')'
                fetch_local(sql, [])
                # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                    stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_no_id)
                print sql
                fetch_local(sql, [])
        # 第四志愿被分配
        elif time.time() >= (start_time+3*24*60*60.0) and time.time() < (start_time+4*24*60*60.0):
            sql = '''SELECT stu_no,volunteer_topic_no_id,MAX(score) FROM app_application a LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no WHERE volunteer_no = 4 AND volunteer_topic_no_id>=0 GROUP  BY volunteer_topic_no_id '''
            rss = fetch_local(sql, [])
            for rs in rss:
                stu_no = rs['stu_no']
                volunteer_topic_no_id = rs['volunteer_topic_no_id']
                sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                    volunteer_topic_no_id) + ',' + str(stu_no) + ',' + str(1) + ')'
                fetch_local(sql, [])
                # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                    stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_no_id)
                print sql
                fetch_local(sql, [])
        # 第五志愿被分配
        elif time.time() >= (start_time+4*24*60*60.0) and time.time() < (start_time+5*24*60*60.0):
            sql = '''SELECT stu_no,volunteer_topic_no_id,MAX(score) FROM app_application a LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no WHERE volunteer_no = 5 AND volunteer_topic_no_id>=0 GROUP  BY volunteer_topic_no_id '''
            rss = fetch_local(sql, [])
            for rs in rss:
                stu_no = rs['stu_no']
                volunteer_topic_no_id = rs['volunteer_topic_no_id']
                sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                    volunteer_topic_no_id) + ',' + str(stu_no) + ',' + str(1) + ')'
                fetch_local(sql, [])
                # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                    stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_no_id)
                print sql
                fetch_local(sql, [])
        # 第六志愿被分配
        elif time.time() >= (start_time+5*24*60*60.0) and time.time() < (start_time+6*24*60*60.0):
            sql = '''SELECT stu_no,volunteer_topic_no_id,MAX(score) FROM app_application a LEFT JOIN app_select_sysuser b ON b.user_id = a.stu_no WHERE volunteer_no = 6 AND volunteer_topic_no_id>=0 GROUP  BY volunteer_topic_no_id '''
            rss = fetch_local(sql, [])
            for rs in rss:
                stu_no = rs['stu_no']
                volunteer_topic_no_id = rs['volunteer_topic_no_id']
                sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                    volunteer_topic_no_id) + ',' + str(stu_no) + ',' + str(1) + ')'
                fetch_local(sql, [])
                # TODO：删除该学生在app_applicaton里的信息，sql，并fetch_local(sql,[])
                sql = '''DELETE FROM app_application WHERE  stu_no=''' + str(
                    stu_no) + ' OR volunteer_topic_no_id=' + str(volunteer_topic_no_id)
                print sql
                fetch_local(sql, [])
        #自由分配start
        elif time.time() >= (start_time+6*24*60*60.0) and time.time() < (start_time+7*24*60*60.0):
            # 自由分配start
            achieve_year = achieveyear()

            # 取到学生和老师人数的的比值
            sql = 'SELECT COUNT(*) numstu FROM app_select_sysuser WHERE role_id =1 AND achieve_year = ' + str(
                achieve_year)
            rss = fetch_local(sql, [])
            stunum = rss[0]['numstu']
            sql = 'SELECT COUNT(*) numtea FROM app_select_sysuser WHERE (role_id=3 OR role_id=4) AND achieve_year = ' + str(
                achieve_year)
            rss = fetch_local(sql, [])
            teanum = rss[0]['numtea']
            num = stunum / teanum
            print num
            sql = 'SELECT id  FROM app_major'''
            rss = fetch_local(sql, [])
            for rs in rss:
                major_id = rs['id']
                print major_id
                print '开始专业'
                # listhigh
                sql = '''SELECT id,tea_no FROM app_topic WHERE tea_no IN 
                                             (SELECT tea_no FROM (SELECT b.tea_no,COUNT(*) num FROM app_application_state a 
                                                                  LEFT JOIN app_topic b ON b.id = a.topic GROUP BY b.tea_no) T1  
                                             WHERE T1.num >=''' + str(num) + ''') AND id NOT IN (SELECT topic FROM app_application_state)
                                             AND year = ''' + str(achieve_year) + ''' AND major_id=''' + str(major_id)
                print sql
                rss = fetch_local(sql, [])

                listhigh = []
                for rs in rss:
                    listhigh.append(rs['id'])

                print 'listhigh'
                print listhigh

                # listlow
                sql = '''SELECT id,tea_no FROM app_topic WHERE tea_no IN 
                                                     (SELECT tea_no FROM (SELECT b.tea_no,COUNT(*) num FROM app_application_state a 
                                                                          LEFT JOIN app_topic b ON b.id = a.topic GROUP BY b.tea_no) T1  
                                                     WHERE T1.num <''' + str(
                    num) + ''') AND id NOT IN (SELECT topic FROM app_application_state) 
                                    AND year = ''' + str(achieve_year) + ''' AND major_id=''' + str(major_id)
                print sql
                rss = fetch_local(sql, [])

                listlow = []
                for rs in rss:
                    listlow.append(rs['id'])

                sql = '''SELECT id FROM app_topic WHERE id NOT IN
                                         (SELECT id FROM app_topic WHERE tea_no IN 
                                                     (SELECT tea_no FROM (SELECT b.tea_no,COUNT(*) num FROM app_application_state a 
                                                                          LEFT JOIN app_topic b ON b.id = a.topic GROUP BY b.tea_no) T1  
                                                     WHERE T1.num <100) AND id NOT IN (SELECT topic FROM app_application_state)
                                                     AND year = ''' + str(achieve_year) + ''')
                                                     AND id NOT IN (SELECT topic FROM app_application_state)
                                                     AND year =''' + str(achieve_year) + ''' AND major_id=''' + str(
                    major_id)
                print sql
                rss = fetch_local(sql, [])
                for rs in rss:
                    listlow.append(rs['id'])

                print 'listlow'
                print listlow
                # list of unselected student未选成功学生池
                sql = '''SELECT user_id FROM app_select_sysuser WHERE role_id=1 AND user_id NOT IN (SELECT selected_stu_no
                                         FROM app_application_state) AND major_id=''' + str(
                    major_id) + ''' AND achieve_year=''' + str(achieve_year)
                print sql
                rss = fetch_local(sql, [])
                listuns = []
                for rs in rss:
                    listuns.append(rs['user_id'])

                print 'listuns'
                print len(listuns)
                print listuns
                # 未被分配的题目池low×2，high×1混合到一起
                listcb = []
                for one in listlow:
                    listcb.append(one)
                    listcb.append(one)
                for oneh in listhigh:
                    listcb.append(oneh)
                print listcb
                local_conn.commit()
                for stu in listuns:
                    selected_stu_no = stu
                    volunteer_topic_no_id = choice(listcb)
                    sql = ''' INSERT INTO `app_application_state`(`topic`, `selected_stu_no`, `submit`) VALUES (''' + str(
                        volunteer_topic_no_id) + ',' + str(selected_stu_no) + ',' + str(1) + ')'
                    fetch_local(sql, [])
                    while listcb.count(volunteer_topic_no_id) > 0:
                        listcb.remove(volunteer_topic_no_id)
                    print '学生和题目分配成功'

            # 自由分配结束
        #自由分配结束
        else:
            print '前面if，elif没进去'
        local_conn.commit()           
        
        print 'end daily task'

    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def startdate():
    try:
        sql = '''SELECT `select3_start` FROM `app_date_setting` WHERE `activation` =1'''
        rss = fetch_local(sql, [])
        start_date = rss[0]['select3_start']
        print str(start_date)
        return start_date
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

def timetypechange(sdate):
    #将其转换为时间数组
    timeArray = time.strptime(sdate, "%Y-%m-%d")
    #转换为时间戳:
    timeStamp = time.mktime(timeArray)
    print timeStamp
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

