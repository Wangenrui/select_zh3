# coding=utf-8

import django
django.setup()

from DBoperater import dictfetchall
from django.core.mail import send_mail
from django.db import connection
from models import *
from mobile import get_area_info

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


SENDER = 'liaoyanghx@aliyun.com'


def send_nortify(company_id, subject, message):
    users = SysUser.objects.filter(company=Company.objects.get(id=company_id))
    for user in users:
        if user.message_type.id == 3 or user.message_type.id == 4:
            send_mail(subject, message, SENDER, [user.email])

        if user.message_type.id == 2 or user.message_type.id == 4:
            print message
            # send_sms(message, '', SENDER, str(user.user_email))



# prepare email subject and message as example
# subject: 起爆信息： 2017年06月12日 辽阳鞍辽矿业有限公司
# 辽阳鞍辽矿业有限公司
#
# 2017年6月27日 鞍辽矿业第三矿区
#
# 实际使用爆材数量：
#
# 炸药：9866kg，普通导爆管雷管：136发。

# item = {}
# item['create_time'] = 1498696899
# btime = strftime('%Y年%m月%d日', localtime(item['create_time'] / 1000))
# area_id = 'a935a45a4c9b4be0a019c471522d4cd1'
# send_email_notification(area_id, btime)

def send_email_notification(area_id, btime):
    area_info = get_area_info(area_id)
    cid = area_info['company_id']
    cname = area_info['company_name']
    aname = area_info['name']
    subject = '起爆信息：' + btime + ' ' + cname
    message = '' + cname + '\n\n'
    message = message + btime + ' ' + aname + '\n\n'
    message = message + '实际使用爆材数量：\n'

    sql_mcount = '''
                SELECT area_id,
                    SUM(dgt_deto_count) AS dgt_deto_count,
                    SUM(ele_deto_count) AS ele_deto_count,
                    SUM(tube_deto_count) AS tube_deto_count,
                    SUM(explosive_count) AS explosive_count,
                    SUM(explosive_count_02W) AS explosive_count_02W,
                    SUM(explosive_count_034) AS explosive_count_034,
                    SUM(explosive_count_03W) AS explosive_count_03W,
                    SUM(explosive_count_03X) AS explosive_count_03X,
                    SUM(nonel_deto_count) AS nonel_deto_count,
                    SUM(fuse_count) AS fuse_count
                FROM
    	        (SELECT area_id,
    	            SUM(CASE WHEN resource_sub_type_id IN (2,13) THEN resource_count ELSE 0 END) AS dgt_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (3,7,10) THEN resource_count ELSE 0 END) AS ele_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (4,5,6,8,9,11,12) THEN (end_index - start_index +1) ELSE 0 END) AS tube_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (14,15,16,17) THEN resource_count ELSE 0 END) AS explosive_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (14) THEN resource_count ELSE 0 END) AS explosive_count_02W,
    	            SUM(CASE WHEN resource_sub_type_id IN (15) THEN resource_count ELSE 0 END) AS explosive_count_034,
    	            SUM(CASE WHEN resource_sub_type_id IN (16) THEN resource_count ELSE 0 END) AS explosive_count_03W,
    	            SUM(CASE WHEN resource_sub_type_id IN (17) THEN resource_count ELSE 0 END) AS explosive_count_03X,
    	            SUM(CASE WHEN resource_sub_type_id IN (19) THEN resource_count ELSE 0 END) AS nonel_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (18) THEN resource_count ELSE 0 END) AS fuse_count
    	            FROM view_materialrecord
    	        WHERE record_type_id=1 AND area_id=%s
    	        UNION ALL
                SELECT area_id,
    	            SUM(CASE WHEN resource_sub_type_id IN (2,13) THEN -resource_count ELSE 0 END) AS dgt_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (3,7,10) THEN -resource_count ELSE 0 END) AS ele_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (4,5,6,8,9,11,12) THEN -(end_index - start_index +1) ELSE 0 END) AS tube_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (14,15,16,17) THEN -resource_count ELSE 0 END) AS explosive_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (14) THEN -resource_count ELSE 0 END) AS explosive_count_02W,
    	            SUM(CASE WHEN resource_sub_type_id IN (15) THEN -resource_count ELSE 0 END) AS explosive_count_034,
    	            SUM(CASE WHEN resource_sub_type_id IN (16) THEN -resource_count ELSE 0 END) AS explosive_count_03W,
    	            SUM(CASE WHEN resource_sub_type_id IN (17) THEN -resource_count ELSE 0 END) AS explosive_count_03X,
    	            SUM(CASE WHEN resource_sub_type_id IN (19) THEN -resource_count ELSE 0 END) AS nonel_deto_count,
    	            SUM(CASE WHEN resource_sub_type_id IN (18) THEN -resource_count ELSE 0 END) AS fuse_count
    	            FROM view_materialrecord
    	        WHERE record_type_id=4 AND area_id=%s) t
    	        GROUP BY area_id
            '''

    cursor = connection.cursor()
    cursor.execute(sql_mcount, [area_id, area_id])
    sql_used_out = dictfetchall(cursor)[0]
    if sql_used_out['area_id'] == None:
        print 'No used matertial record for area ' + area_id
    else:

        if 0 != sql_used_out['dgt_deto_count']:
            message = message + '电子数码雷管(发): ' + str(sql_used_out['dgt_deto_count']) + '; '
        if 0 != sql_used_out['tube_deto_count']:
            message = message + '非电导爆管(发): ' + str(sql_used_out['tube_deto_count']) + '; '
        if 0 != sql_used_out['nonel_deto_count']:
            message = message + '塑料导爆管(米): ' + str(sql_used_out['nonel_deto_count']) + '; '
        if 0 != sql_used_out['fuse_count']:
            message = message + '导爆索(米): ' + str(sql_used_out['fuse_count']) + '; '

        message = message + '\n'

        if sql_used_out['explosive_count_02W'] != 0:
            message = message + '乳化炸药(公斤): ' + str(sql_used_out['explosive_count_02W']).rstrip('0').rstrip('.') + '; '
        if sql_used_out['explosive_count_034'] != 0:
            message = message + '粉状炸药(公斤): ' + str(sql_used_out['explosive_count_034']).rstrip('0').rstrip('.') + '; '
        if sql_used_out['explosive_count_03W'] != 0:
            message = message + '改性铵油(公斤): ' + str(sql_used_out['explosive_count_03W']).rstrip('0').rstrip('.') + '; '
        if sql_used_out['explosive_count_03X'] != 0:
            message = message + '胶质炸药(公斤): ' + str(sql_used_out['explosive_count_03X']).rstrip('0').rstrip('.') + '; '

        message = message + '\n'

    print subject
    print message
    send_nortify(cid, subject, message)
