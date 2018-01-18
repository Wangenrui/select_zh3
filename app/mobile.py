# coding=utf-8

from DBoperater import uuidToString, dictfetchall, pc
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from models import *
from rest_framework import renderers
from time import strftime, localtime
import base64
import django
django.setup()
import json
import datetime
import sys
import urllib
from hashlib import md5


def MD5Digest(text):
    return md5(text).digest()


def sys_info():
    info = "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
    print info
    return


def now():
    current = datetime.datetime.now()
    # current = timezone.now()
    return current.strftime('%Y-%m-%d %H:%M:%S')


def get_equip_id(equip_code):
    try:
        cursor = connection.cursor()
        sql = 'SELECT id AS equip_id FROM app_equipment WHERE equipment_code=\''+equip_code+'\''
        cursor.execute(sql)
        equipment = dictfetchall(cursor)[0]
        return equipment['equip_id']
    except:
        sys_info()
        return ''


def get_area_info(area_id):
    try:
        cursor = connection.cursor()
        #sql = '''SELECT b.province_id, b.city_id, b.county_id, b.police_company_id, a.company_id, a.project_id
	    #    FROM app_area a
	    #    LEFT JOIN app_project b ON b.id=a.project_id
	    #    WHERE a.id = '''

        sql = '''SELECT a.province_id, a.city_id, a.county_id, a.police_company_id, a.company_id, a.company_name, a.project_id, a.name
	        FROM view_area a
	        WHERE a.id = '''

        sql = sql + '\'' + area_id + '\''
        cursor.execute(sql)
        return dictfetchall(cursor)[0]
    except:
        sys_info()
        return {}


def safed(req):
    return render_to_response('safed.html')


# getLoginServerAddress()
#     getServer1Address() + "/service/v1/auth/login"
# http post
# http://182.92.190.30:9210/service/v1/auth/login
# params: user_name=zhiwen&password=111111
#     response = JsonResponse({"tag": "", "success": True}, safe=False)
#     response = JsonResponse({'tag': '用户名或密码错误', 'success': False}, safe=False)

def mlogin(req):
    response = JsonResponse({'tag': '用户名或密码错误', 'success': False}, safe=False)
    try:
        if req.method == 'POST':
            user_name = req.POST.get('user_name', '')
            password = req.POST.get('password', '')

            user = SysUser.objects.filter(user_id__exact=user_name, password__exact=pc.encrypt(password), is_login=True)
            if user:
                response = JsonResponse({"tag": "", "success": True}, safe=False)

                company_id = user[0].company_id
                response.set_cookie('usercode', user_name, 43200)

                return response
        return response
    except:
        sys_info()
        return response


# getUserInfoServerAddress()
# ocean: getServer1Address() + "/app/muser_info";
# zy:    getServer1Address() + "/service/v1/scanner/current_company/info";
# http get
# No params
#     {
#     	"person_name": "\u5218\u516d\u516d",
#     	"company_short_name": "\u6210\u8fdc",
#     	"roles": [{
#     		"code": 11,
#     		"name": "爆破员"
#     	}],
#     	"company_id": "159e42ae569411e5b713dea90594582e",
#     	"version": 1,
#     	"company_name": "\u8fbd\u5b81\u6210\u8fdc",
#     	"person_id": "d0274680603b11e5a417dea90594582e",
#     	"success": true
#     }

def muser_info(req):
    try:
        if req.method == 'GET':
            company_id = req.COOKIES.get('company_id', '')
            user_id = req.COOKIES.get("usercode", '')

            id = SysUser.objects.get(user_id=user_id)
            uid = uuidToString(str(id.id))

            cursor = connection.cursor()
            cursor.execute('''
                SELECT a.id AS person_id, a.user_name AS person_name,
                    b.id as company_id, b.company_name, b.company_short_name
                FROM app_sysuser a
                LEFT JOIN app_company b ON b.id=a.company_id
                WHERE a.user_id = %s
            ''', [user_id])

            dict = dictfetchall(cursor)[0]
            dict['person_id'] = uuidToString(str(dict['person_id']))
            dict['company_id'] = uuidToString(str(dict['company_id']))
            dict['success'] = True
            dict['version'] = 1

            cursor.execute('''
                SELECT (a.certificate_type_id + 8) AS code, b.cert_name AS name
                FROM app_sysuser a
                LEFT JOIN app_certificatetype b ON b.id=a.certificate_type_id
                WHERE a.id = %s
            ''', [uid])

            dict['roles'] = dictfetchall(cursor)
            return HttpResponse(json.dumps(dict))
        return render_to_response('403.html')
    except:
        sys_info()
        return render_to_response('403.html')

# getEquipAuthAddress()
#     getServer1Address() + "/service/v1/equipment/auth2?" + "equip_id=" + "861189014120793"
# http get
# MD5(equip_id + "dqpmchtx1122334455!!@@") => "code"
#     return Base64.encodeToString(MessageDigest.getInstance("MD5").digest(code.getBytes("utf-8")), 0);
# no params
# {
# 	"code": "lzu4AHXebPn3BXLRVw+Xgg==\n",
# 	"success": true
# }

# Algorithm needs to be updated. Current is wrong. Or get from current platform by deviceID

def mget_equip_auth(req):
    try:
        if req.method == 'GET':
            equip_id = req.GET.get('equip_id', '')
            equipment = Equipment.objects.get(equipment_code=equip_id)
            if not equipment:
                return JsonResponse({'code': '', 'success': False}, safe=False)
            else:
                equip_id = equip_id + 'dqpmchtx1122334455!!@@'
                code = base64.b64encode(MD5Digest(equip_id.encode('utf-8')))
                return JsonResponse({'code': code+'\n', 'success': True}, safe=False)

        return JsonResponse({'code': '', 'success': False}, safe=False)
    except:
        sys_info()
        return JsonResponse({'code': '', 'success': False}, safe=False)


# getReprotBlastRecordUri()
#    getServer1Address() + "/service/v1/scanner/blast_record";
# http post = > referring to getReprotBlastRecordUri.json
# example
# {
#     "equip_id": "",
#     "items": [{
#             "id": "id",
#             "blast_type": "blast_type",
#             "create_time": "create_time",
#             "position_x": "position_x",
#             "position_y": "position_y",
#             "user1_id": "user1_id",
#             "user2_id": "user2_id",
#             "user3_id": "user3_id",
#             "user4_id": "user4_id",
#             "blast_area_id": "blast_area_id",
#             "blast_mode": "blast_mode",
#             "blast_auth_user1_id": "blast_auth_user1_id",
#             "blast_auth_user2_id": "blast_auth_user2_id",
#             "soc_deto_items": [{
#                     "id": "id1",
#                     "state": "state1"
#                 },...
#             ]
#         },...
#     ]
# }


def mblast_record(req):
    response = JsonResponse({'success': False}, safe=False)
    try:
        if req.method == 'POST':
            rj = req.body.replace('data=', '')
            rj = urllib.unquote(rj)
            rj = json.loads(rj)
            equipment_id = get_equip_id(rj['equip_id'])
            items = rj['items']

            for item in items:
                # id = uuid() # new generated or from equipment
                # "user3_id": "user3_id", # from equipment,
                # "user4_id": "user4_id", # from equipment,
                # `deto_transfer_record_id` varchar(32) # from database,
                area_id = item['blast_area_id']
                area_info = get_area_info(area_id)

                blast_record = BlastRecord(
                    id=item['id'],
                    province=Province.objects.get(id=area_info['province_id']),
                    city=City.objects.get(id=area_info['city_id']),
                    county=County.objects.get(id=area_info['county_id']),
                    company=Company.objects.get(id=area_info['company_id']),
                    police_company_id = area_info['police_company_id'],
                    project=Project.objects.get(id=area_info['project_id']),
                    area=Area.objects.get(id=area_id),
                    equipment=Equipment.objects.get(id=equipment_id),
                    user1_id=item['user1_id'],
                    user2_id=(item['user2_id'] if item.has_key('user2_id') else ''),
                    blast_auth_user1_id=(item['blast_auth_user1_id'] if item.has_key('blast_auth_user1_id') else ''),
                    blast_auth_user2_id=(item['blast_auth_user2_id'] if item.has_key('blast_auth_user2_id') else ''),
                    blast_type=BlastType.objects.get(id=item['blast_mode']),
                    blast_mode=BlastMode.objects.get(id=item['blast_type']),
                    create_time=now(),
                    blasting_time=strftime("%Y-%m-%d %H:%M:%S", localtime(item['create_time']/1000)),
                    longitude=item['position_x'],
                    latitude=item['position_y']
                )
                blast_record.save()

                soc_deto_items = item['soc_deto_items']
                for soc_deto_item in soc_deto_items:
                    material_record = MaterialRecord.objects.get(id=soc_deto_item['id'])
                    material_record.deto_status=soc_deto_item['state']
                    material_record.save()

                #btime = strftime('%Y年%m月%d日', localtime(item['create_time'] / 1000))
                #send_email_notification(area_id, btime)

            response = JsonResponse({"success": True}, safe=False)
            return response
        return response
    except:
        sys_info()
        return response


# getReprotScanRecordUri()
#     getServer1Address() + "/service/v1/scanner/scan_record";
# http post => referring to getReprotScanRecordUri.json
# {
#     "items": [{
#         "id": "bcecb7920aea452a80d00339a5ad1c0c"
#         "blast_area_id": "6975d20d0d9f452aa65dd78af02e8a17",
#         "from_user1_id": "617465c74c62486bb40c0d10ae367b48",
#         "to_user1_id": "bb75d520957e49a398111a126e140c77",
#         "total_count": 256,
#         "circulation_type": 1,
#         "create_time": 1493393505977,
#         "position_x": 123.092874,
#         "position_y": 41.216403,
#         "scan_resource_type": 2, #0 - DetonatorRangeItem, 1 - ExplosiveRangeItem, 2 - NoCodeExplosiveItem
#         "items": [{
#             "count": "256",
#             "type": 1,
#             "id": "2b4e5b65341e45418e09abf2b2145bc6",
#             "sub_type": "02W"
#         }],
#     }],
#     "equip_id": "861189014120793"
# }

# {
#     "equip_id": "",
#     "items": [{
#         "from_user1_id": "example",
#         "from_user2_id": "example",
#         "to_user1_id": "example",
#         "to_user2_id": "example",
#         "items": [{ #0 - DetonatorRangeItem,
#                 "id": "example",
#                 "start_index": "example",
#                 "end_index": "example",
#                 "main_code": "example",
#                 "main_simple_code": "example",
#                 "type": "example",
#                 "sub_type": "example",
#             },
#             { 1 - ExplosiveRangeItem
#                 "id": "example",
#                 "start_index": "example",
#                 "end_index": "example",
#                 "main_code": "example",
#                 "main_simple_code": "example",
#                 "type": "example",
#                 "sub_type": "example",
#                 "unit": "example",
#             },
#             { 2 - NoCodeExplosiveItem
#                 "id": "example",
#                 "type": "example",
#                 "sub_type": "example",
#                 "count": "example"
#             }
#         ]
#     }]
# }

def mscan_record(req):
    response = JsonResponse({'success': False}, safe=False)
    try:
        if req.method == 'POST':
            rj = req.body.replace('data=', '')
            rj = urllib.unquote(rj)
            rj = json.loads(rj)

            equipment_id = get_equip_id(rj['equip_id'])
            items = rj['items']

            for item in items:
                # id = uuid() # new generated or from equipment
                area_id = item['blast_area_id']
                area_info = get_area_info(area_id)
                area = Area.objects.get(id=area_id)
                record_type = TransferRecordType.objects.get(id=item['circulation_type'])
                resource_type = MaterialType.objects.get(id=item['scan_resource_type'])

                transfer_record = Transfer(
                    id=item['id'],
                    province=Province.objects.get(id=area_info['province_id']),
                    city=City.objects.get(id=area_info['city_id']),
                    county=County.objects.get(id=area_info['county_id']),
                    company=Company.objects.get(id=area_info['company_id']),
                    police_company_id = area_info['police_company_id'],
                    project=Project.objects.get(id=area_info['project_id']),
                    area=area,
                    equipment=Equipment.objects.get(id=equipment_id),
                    from_user1_id = item['from_user1_id'],
                    from_user2_id = (item['from_user2_id'] if item.has_key('from_user2_id') else ''),
                    to_user1_id = item['to_user1_id'],
                    to_user2_id = (item['to_user2_id'] if item.has_key('to_user2_id') else ''),
                    resource_count = item['total_count'],
                    record_type=record_type,
                    resource_type=resource_type,
                    create_time=now(),
                    transfer_time= strftime("%Y-%m-%d %H:%M:%S", localtime(item['create_time']/1000)),
                    longitude=item['position_x'],
                    latitude=item['position_y']
                )
                transfer_record.save()

                sub_items = item['items']
                for sub_item in sub_items:
                    # "type": "example", # from equipment
                    # soc_code # from database
                    # produce_code # from database
                    # simple_code # from database
                    # version_id # from database
                    # deto_status # from database

                    start_index = sub_item['start_index'] if sub_item.has_key('start_index') else 0
                    end_index = sub_item['end_index'] if sub_item.has_key('end_index') else 0
                    resource_count = sub_item['count'] if sub_item.has_key('count') else 0
                    if resource_type == 0 or resource_type == 1:
                        resource_count = end_index - start_index + 1

                    material_record = MaterialRecord(
                        id=sub_item['id'],
                        record=transfer_record,
                        area=area,
                        #user=SysUser.objects.get(id=item['to_user1_id']), # 安全员
                        user=SysUser.objects.get(id=item['from_user1_id']), # 爆破员
                        record_type=record_type,
                        resource_type=resource_type,
                        resource_sub_type=MaterialSubType.objects.get(code=sub_item['sub_type']),
                        main_code=(sub_item['main_code'] if sub_item.has_key('main_code') else ''),
                        simple_code=(sub_item['main_simple_code'] if sub_item.has_key('main_simple_code') else ''),
                        start_index=start_index,
                        end_index=end_index,
                        resource_count=resource_count,
                        unit=(sub_item['unit'] if sub_item.has_key('unit') else 0)
                    )
                    material_record.save()

            response = JsonResponse({"success": True}, safe=False)
            return response
        return response
    except:
        sys_info()
        return response


# getReprotPersonSignInRecordUri()
#     getServer1Address() + "/service/v1/scanner/district_sign_record";
# http post => referring to getReprotPersonSignInRecordUri.json
#
# {
#   "equip_id": "",
#   "items": [
#     {
#       "blast_area_id": "example",
#       "blast_area_name": "example",
#       "create_time": "example",
#       "id": "example",
#       "position_x": "example",
#       "position_y": "example",
#       "sign_in_type": "example",
#       "user_id": "example",
#       "user_name": "example"
#     }
#   ]
# }

def mdistrict_sign_record(req):
    response = JsonResponse({'success': False}, safe=False)
    try:
        if req.method == 'POST':
            rj = req.body.replace('data=', '')
            rj = urllib.unquote(rj)
            rj = json.loads(rj)
            equipment_id = get_equip_id(rj['equip_id'])
            items = rj['items']

            for item in items:
                # need to judge if user are assigned to a project, and if current position is at assigned area
                # need also to judge the user sign-in type to enable different features
                user = SysUser.objects.get(id=item['id'])
                if not user:
                    response = JsonResponse({'success': False}, safe=False)
                    break

            response = JsonResponse({"success": True}, safe=False)
            return response
        return response
    except:
        sys_info()
        return response


# getReprotTransportRecordUri()
#     getServer1Address() + "/service/v1/scanner/transport_record";
# http post => referring to getReprotTransportRecordUri.json
#
# {
#     "equip_id": "",
#     "items": [{
#         "id": "example",
#         "user1_id": "example",
#         "user1_name": "example",
#         "user2_id": "example",
#         "user2_name": "example",
#         "resource_type": "example",
#         "car_code": "example",
#         "create_time": "example",
#         "status": "example",
#         "blast_area_id": "example",
#         "blast_area_name": "example",
#         "resource_count": "example"
#     }]
# }

def mtransport_record(req):
    response = JsonResponse({'success': False}, safe=False)
    try:
        if req.method == 'POST':
            rj = req.body.replace('data=', '')
            rj = urllib.unquote(rj)
            rj = json.loads(rj)
            equipment_id = get_equip_id(rj['equip_id'])
            items = rj['items']

            for item in items:
                # "user2_id": "example", # from equipment
                # "status": "example", # from equipment

                # id = uuid() # new generated or from equipment
                area_id = item['blast_area_id']
                area_info = get_area_info(area_id)
                area = Area.objects.get(id=area_id)

                record = Transport(
                    id=item['id'],
                    province=Province.objects.get(id=area_info['province_id']),
                    city=City.objects.get(id=area_info['city_id']),
                    county=County.objects.get(id=area_info['county_id']),
                    company=Company.objects.get(id=area_info['company_id']),
                    police_company_id=area_info['police_company_id'],
                    project=Project.objects.get(id=area_info['project_id']),
                    area=area,
                    equipment=Equipment.objects.get(id=equipment_id),
                    user=SysUser.objects.get(id=item['user1_id']),
                    car_code=item['car_code'],
                    resource_count=item['resource_count'],
                    resource_type=ResourceType.objects.get(id=item['resource_type']),
                    create_time=now(),
                    transport_time=strftime("%Y-%m-%d %H:%M:%S", localtime(item['create_time']/1000)),
                )
                record.save()

            response = JsonResponse({"success": True}, safe=False)
            return response
        return response
    except:
        sys_info()
        return response


# getApplicationDictFileServerUri()
#   getServer1Address() + "/type_config/application_dict.json";
# No params:
#   {'deto_types': [{'type': 1, 'name': '导爆管雷管'}, {'type': 2, 'name': '电雷管'}, {'type': 3, 'name': '数码雷管'}], 'create_time': '2015-11-06 12:15:00', 'version': 1, 'deto_code_types': [{'code': 'no', 'type': 3, 'name': '未知类型'}, {'code': 'smlg', 'type': 3, 'name': '数码雷管'}, {'code': 'dlg', 'type': 1, 'name': '电雷管'}, {'code': 'dbg', 'type': 1, 'name': '导爆管雷管'}, {'code': 'r', 'type': 1, 'name': '毫秒导爆管雷管'}, {'code': 'q', 'type': 1, 'name': '半秒导爆管雷管'}, {'code': 's', 'type': 1, 'name': '普通秒点电雷管'}, {'code': 'a', 'type': 1, 'name': '抗水半秒导爆管雷管'}, {'code': 'b', 'type': 1, 'name': '抗水毫秒导爆管雷管'}, {'code': 'b', 'type': 1, 'name': '地震勘探电雷管'}, {'code': 'c', 'type': 1, 'name': '抗水秒导爆管雷管'}, {'code': 'd', 'type': 1, 'name': '抗水顺发导爆管雷管'}, {'code': 'J', 'type': 3, 'name': '数码雷管'}], 'protected_object_types': [{'transmission_v_range': [[0.15, 0.45], [0.45, 0.9], [0.9, 1.5]], 'type': 1, 'name': '土窑洞'}, {'transmission_v_range': [[0.15, 0.45], [0.45, 0.9], [0.9, 1.5]], 'type': 2, 'name': '土坯房'}, {'transmission_v_range': [[0.15, 0.45], [0.45, 0.9], [0.9, 1.5]], 'type': 3, 'name': '毛石房屋'}, {'transmission_v_range': [[1.5, 2.0], [2.0, 2.5], [2.5, 3.0]], 'type': 4, 'name': '一般民用建筑物'}, {'transmission_v_range': [[2.5, 3.5], [3.5, 4.5], [4.2, 5.0]], 'type': 5, 'name': '工业商业建筑物'}, {'transmission_v_range': [[0.1, 0.2], [0.2, 0.3], [0.3, 0.5]], 'type': 6, 'name': '一般古建筑古迹'}, {'transmission_v_range': [[0.5, 0.6], [0.6, 0.7], [0.7, 0.9]], 'type': 7, 'name': '运行水电站'}, {'transmission_v_range': [[0.5, 0.6], [0.6, 0.7], [0.7, 0.9]], 'type': 8, 'name': '发电厂中心控制室'}, {'transmission_v_range': [[7, 8], [8, 10], [10, 15]], 'type': 9, 'name': '水工隧道'}, {'transmission_v_range': [[10, 12], [12, 15], [15, 20]], 'type': 10, 'name': '交通隧道'}, {'transmission_v_range': [[15, 18], [18, 25], [20, 30]], 'type': 11, 'name': '矿山巷道'}, {'transmission_v_range': [[5, 9], [8, 12], [10, 15]], 'type': 12, 'name': '永久岩石边坡'}, {'transmission_v_range': [[1.5, 2.0], [2.0, 2.5], [2.5, 3.0]], 'type': 13, 'name': '新浇大体积混凝土(3天内)'}, {'transmission_v_range': [[3.0, 4.0], [4.0, 5.0], [5.0, 7.0]], 'type': 14, 'name': '新浇大体积混凝土(7天内)'}, {'transmission_v_range': [[7.0, 8.0], [8.0, 10.0], [10.0, 12.0]], 'type': 15, 'name': '新浇大体积混凝土(28天内)'}], 'explosive_code_types': [{'code': '02W', 'unit_type': 2, 'prompt': '单位公斤', 'type': 1, 'name': '乳化炸药'}, {'code': '034', 'unit_type': 2, 'prompt': '单位公斤', 'type': 1, 'name': '粉状'}, {'code': '03W', 'unit_type': 2, 'prompt': '单位公斤', 'type': 1, 'name': '改性铵油'}, {'code': '03X', 'unit_type': 2, 'prompt': '单位公斤', 'type': 1, 'name': '胶质'}, {'code': '25B', 'unit_type': 1, 'prompt': '单位米', 'type': 2, 'name': '导爆索'}, {'code': '25H', 'unit_type': 1, 'prompt': '单位米', 'type': 2, 'name': '塑料导爆管'}], 'project_blast_types': [{'shake_hz': [0, 20], 'type': 1, 'name': '硐室爆破'}, {'shake_hz': [10, 60], 'type': 2, 'name': '露天深孔爆破'}, {'shake_hz': [40, 100], 'type': 3, 'name': '露天浅孔爆破'}, {'shake_hz': [30, 100], 'type': 4, 'name': '地下深孔爆破'}, {'shake_hz': [60, 300], 'type': 5, 'name': '地下浅孔爆破'}]}

def mapplication_dict(req):
    return render_to_response('application_dict.json')


# getExplosiveAreaServerUri()
#     getServer1Address() + "/service/v1/scanner/current_equipment/burst_districts";
# URL: + ?data={'company_id':'','equip_id'=''}
# Example: /service/v1/scanner/current_equipment/burst_districts?data={'company_id':'159e42ae569411e5b713dea90594582e','equip_id'='861189014120793'}
# After URLEncoder.encode(Example.toString(), "utf-8");
# /service/v1/scanner/current_equipment/burst_districts?data=%7B%22equip_id%22%3A%22861189014120793%22%2C%22company_id%22%3A%22159e42ae569411e5b713dea90594582e%22%7D
# Need to URLDecode
# http get => referring to getExplosiveAreaServerUri.json
# {
#     "work_status": 1,
#     "success": true,
#     "valid_time": 1636473600,
#     "blast_areas": [{
#         "position_y": 35.023,
#         "radius": 2000.0,
#         "id": "0596b3cfc82011e68b0bda932e028508",
#         "position_x": 118.34,
#         "name": "\u80a1\u6362\u80a1"
#     }],
#     "version": 1,
#     "create_time": "2016-12-22 16:24:27"
# }

def mburst_districts(req):
    dict = {}
    dict['work_status'] = 1
    dict['version'] = 1
    dict['create_time'] = now()
    dict['success'] = True
    dict['blast_areas'] = []

    try:
        if req.method == 'GET':
            rj = req.GET.get('data', '').replace('\'', '\"')
            rjl = json.loads(rj)
            equipment_id = rjl['equip_id']
            company_id = rjl['company_id']

            # get equipment valid time by equipment id
            cursor = connection.cursor()
            sql = 'SELECT TIMESTAMPDIFF(SECOND, \'1970-01-01\', valid_time) - 28800 AS valid_time FROM app_equipment WHERE equipment_code=\'' +equipment_id+ '\''

            cursor.execute(sql)
            equipment = dictfetchall(cursor)[0]
            dict['valid_time'] = equipment['valid_time']

            # get blast area info by company id
            # add status=2 => only 'jinxingzhong' area can be used
            sql = 'SELECT id, name, gps_latitude AS position_y, gps_longitude AS position_x, radius FROM app_area WHERE status_id=2 AND company_id=\'' +company_id+ '\''

            cursor.execute(sql)

            # to convert Decimal(x.y) in sql output to x.y
            str = renderers.JSONRenderer().render(dictfetchall(cursor))
            dict['blast_areas'] = json.loads(str)
        else:
            dict['success'] = False
    except:
        sys_info()
        dict['success'] = False
    return HttpResponse(json.dumps(dict))


# getPersonsServerUri()
#     getServer1Address() + "/service/v1/scanner/burst_persons";
# http get
# data={"equip_id":"861189014120793","company_id":"159e42ae569411e5b713dea90594582e","start":1,"limit":20,"name":"liu"}
# /service/v1/scanner/burst_persons?data=%7B%22equip_id%22%3A%22861189014120793%22%2C%22company_id%22%3A%22159e42ae569411e5b713dea90594582e%22%2C%22start%22%3A1%2C%22limit%22%3A20%7D
# {
#     "total": 111,
#     "data": [{
#         "fullname": "77777",
#         "id": "881afe2e6f2d11e59bebdea90594582e",
#         "user_type": 6
#     }, {
#         "fullname": "\u4ecb\u7ecd\u7684",
#         "id": "c81af75e926911e59771da932e028508",
#         "user_type": 4
#     }],
#     "version": 1,
#     "success": true
# }

def mburst_persons(req):
    dict = {}
    dict['version'] = 1
    dict['success'] = True
    dict['total'] = 0
    dict['data'] = []

    try:
        if req.method == 'GET':
            rj = req.GET.get('data', '').replace('\'', '\"')
            rj = json.loads(rj)

            equipment_id = rj['equip_id']
            company_id = rj['company_id']
            offset = rj['start']   # offset is start from 0
            limit = rj['limit']
            #user_name = rj['name']

            # get total user number by company_id and user type
            cursor = connection.cursor()

            sql = 'SELECT COUNT(*) AS total FROM app_sysuser WHERE reg_status = 1 AND certificate_type_id IN (3,4,5,6) AND company_id=\'' +company_id+ '\''
            cursor.execute(sql)
            total = dictfetchall(cursor)[0]
            dict['total'] = total['total']

            # get user info by company id, user type, start and limit
            sql = 'SELECT id, user_name as fullname, certificate_type_id AS user_type FROM app_sysuser WHERE reg_status = 1 AND certificate_type_id IN (3,4,5,6)'
            sql = sql + ' AND company_id=\'' +str(company_id)+ '\'' + ' LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
            cursor.execute(sql)
            dict['data'] = dictfetchall(cursor)
    except:
        sys_info()
        dict['success'] = False
    return HttpResponse(json.dumps(dict))


# getCompanysServerUri()
#     getServer1Address() + "/service/v1/scanner/burst_companys";
# http get
# data={"limit":10,"equip_id":"861189014119126","start":0,"name":"成远"}
# http://182.92.190.30:9210/service/v1/scanner/burst_companys?data={"limit":10,"equip_id":"861189014119126","start":0}
# http://182.92.190.30:9210/service/v1/scanner/burst_companys?data=%7B%22limit%22%3A10%2C%22equip_id%22%3A%22861189014119126%22%2C%22start%22%3A0%7D
# {
#     "data": [{
#         "id": "de10832128f911e5aa389b584ff2af36",
#         "name": " 小唐爆破公司"
#     }],
#     "total": 147,
#     "success": true,
#     "version": 1
# }

def mburst_companys(req):
    dict = {}
    dict['version'] = 1
    dict['success'] = True
    dict['total'] = 0
    dict['data'] = []

    try:
        if req.method == 'GET':
            rj = req.GET.get('data', '').replace('\'', '\"')
            rj = json.loads(rj)
            equipment_id = rj['equip_id']
            offset = rj['start']
            limit = rj['limit']

            # get total user number by company_id and user type
            cursor = connection.cursor()

            sql = 'SELECT COUNT(*) AS total FROM app_company WHERE company_type_id=4'
            cursor.execute(sql)
            total = dictfetchall(cursor)[0]
            dict['total'] = total['total']

            # get user info by company id, user type, start and limit
            sql = 'SELECT id, company_name AS name FROM app_company WHERE company_type_id=4'
            sql = sql + ' LIMIT ' + str(limit) + ' OFFSET ' + str(offset)
            cursor.execute(sql)
            dict['data'] = dictfetchall(cursor)
    except:
        sys_info()
        dict['success'] = False
    return HttpResponse(json.dumps(dict))


# getUploadFingerServerUri()
#     getServer1Address() + "/service/v1/scanner/finger";
# http post
# request body:
# data=%7B%22user_type%22%3A3%2C%22company_id%22%3A%22159e42ae569411e5b713dea90594582e%22%2C%22user_id%22%3A%2210d87cc0619611e58855dea90594582e%22%2C%22user_name%22%3A%22%E5%90%B4%E4%BA%94%22%2C%22finger_data%22%3A%22ywkHZqGq%2BpTFR35QzG2CbKmaDGi7tBR0l2wccLXmpIyp2ZlxaGpzCtxE7liaaipYt5hdC6CN3wr7%5C%5CnGKx1Q7gsCf31a5rY66uqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%5C%5CnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%5C%5CnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%5C%5CnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA%3D%3D%5C%5Cn%22%2C%22id%22%3A%227f5b71382bb341878f66dd3469576a66%22%7D
#
# data = {
#     "user_type": 3,
#     "company_id": "159e42ae569411e5b713dea90594582e",
#     "user_id": "10d87cc0619611e58855dea90594582e",
#     "user_name": "吴五",
#     "finger_data": "ywkHZqGq+pTFR35QzG2CbKmaDGi7tBR0l2wccLXmpIyp2ZlxaGpzCtxE7liaaipYt5hdC6CN3wr7\\nGKx1Q7gsCf31a5rY66uqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\\n",
#     "id": "7f5b71382bb341878f66dd3469576a66"
# }


def mfinger_add(req):
    response = JsonResponse({'success': False}, safe=False)
    company_id = req.COOKIES.get('company_id', '')
    user_name = req.COOKIES.get('usercode', '')
    print 'Finger Add: ' + user_name
    if user_name != 'zhiwen':
        return response

    try:
        if req.method == 'POST':
            rj = req.body.replace('data=', '')
            rj = urllib.unquote(rj)
            rj = json.loads(rj)
            id = rj['id']
            user_id = rj['user_id']
            finger_data = rj['finger_data']
            user = SysUser.objects.get(id=user_id)

            record = Finger(
                id=id,
                user=user,
                finger_data=finger_data
            )
            record.save()

            response = JsonResponse({"success": True}, safe=False)
            return response

        return response
    except:
        sys_info()
        return response


# deleteSingleFingerServerUri()
#     getServer1Address() + "/service/v1/scanner/finger";
# http delete
# http://182.92.190.30:9210/service/v1/scanner/finger/26e4d1cc55ee4dc5a02c0c61739cee71
# finger_id

def mfinger_delete(req, param):
    response = JsonResponse({'success': False}, safe=False)
    company_id = req.COOKIES.get('company_id', '')
    user_name = req.COOKIES.get('usercode', '')
    print 'Finger Delete: ' + user_name
    if user_name != 'zhiwen':
        return response

    try:
        if req.method == 'DELETE':
            Finger.objects.get(id=param).delete()
            return JsonResponse({"success": True}, safe=False)

        return response
    except:
        sys_info()
        return response


# getDownloadFingerServerUri()
#     getServer1Address() + "/service/v1/scanner/company_burst_person/fingers";
# http get
# http://182.92.190.30:9210/service/v1/scanner/company_burst_person/fingers?data=%7B%22equip_id%22%3A%22861189014119126%22%2C%22company_id%22%3A%22159e42ae569411e5b713dea90594582e%22%7D
# data={"equip_id":"861189014119126","company_id":"159e42ae569411e5b713dea90594582e"}
# referring to getDownloadFingerServerUri.json
# {
#   "user_fingers": [
#     {
#       "user_name": "吴五",
#       "user_id": "10d87cc0619611e58855dea90594582e",
#       "user_type": 3,
#       "fingers": [
#         {
#           "id": "7f5b71382bb341878f66dd3469576a66",
#           "value": "ywkHZqGq+pTnAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         }
#       ]
#     },
#     {
#       "user_name": "盛爆2",
#       "user_id": "1dacdf00659111e594a3dea90594582e",
#       "user_type": 3,
#       "fingers": [
#         {
#           "id": "26e4d1cc55ee4dc5a02c0c61739cee71",
#           "value": "ywkPYqGqupRFR75wTW1CbKqbDHi7thR0l2wccLfmpJyr+dnxeGp7M3EAl8Cb15sOJrfY+msLHuj\ncAxRYa6kM3AZqGZK6smC90OfjOojn/T8hn6q7oizZjEw+mYHTHmdaZ+1Nq9atlYAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         },
#         {
#           "id": "33980497f37c4dbdb36a950b94583814",
#           "value": "ywkOXKGqmhTFxv5gze0CdKsbDHC7N5R4lW+cfLTg5ICoxbkJKItrV/REulUibvZuBJQUdGa4PCzZ\nEl8eDW60e0A4/UgP6Fn2g064Ahl+Lw7yvFySOtB9sG24vKi6XFoLWSm1NgAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         },
#         {
#           "id": "7bcd786293554724bd954507699fc297",
#           "value": "ywkPZKGqhZQ7RYGQMW56fGobzHQ6N5R4lW+cfLXgJICvxVgJ75uCTIhF33wwbZdD5ZxGRDS4rVgq\nUB9M6L6HxVIZngxDKe8I/sNZRHZmmcvThlzRyYXzTqURklxX/fzbFui1Nk6ytlYAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         }
#       ]
#     }
#   ],
#   "version": 1,
#   "success": true
# }

def mfingers_company(req):
    company_id = req.COOKIES.get('company_id', '')
    user_name = req.COOKIES.get('usercode', '')
    print 'Finger Company: ' + user_name

    dict = {}
    dict['version'] = 1
    dict['success'] = True
    dict['user_fingers'] = []

    if user_name != 'zhiwen':
        dict['success'] = False
        return HttpResponse(json.dumps(dict))

    try:
        if req.method == 'GET':
            rj = req.GET.get('data', '')
            rj = json.loads(rj)
            equipment_id = rj['equip_id']
            company_id = rj['company_id']

            cursor = connection.cursor()
            sql = 'SELECT * FROM view_finger WHERE company_id=\'' +company_id+ '\''
            cursor.execute(sql)
            results = dictfetchall(cursor)

            user_fingers = {}
            for result in results:
                user_id = result['user_id']
                finger = {"id":result['id'], "value":result['finger_data']}

                if user_id in user_fingers.keys():
                    user_fingers[user_id]["fingers"].append(finger)
                else:
                    user_fingers[user_id] = {
                        "user_name": result['user_name'],
                        "user_id": user_id,
                        "user_type": result['user_type'],
                        "fingers": [finger]
                    }

            for each in user_fingers:
                dict['user_fingers'].append(user_fingers[each])

    except:
        sys_info()
        dict['success'] = False
    return HttpResponse(json.dumps(dict))


# getDownloadProjectFingerServerUri()
#     getServer1Address() + "/service/v1/scanner/project_burst_person/fingers";
# http get
# http://182.92.190.30:9210/service/v1/scanner/project_burst_person/fingers?data=%7B%22equip_id%22%3A%22861189014119126%22%2C%22company_id%22%3A%22159e42ae569411e5b713dea90594582e%22%7D
# data={"equip_id":"861189014119126","company_id":"159e42ae569411e5b713dea90594582e"}
# referring to getDownloadProjectFingerServerUri.json
#
# {
#   "self_user_fingers": [
#     {
#       "user_name": "盛爆2",
#       "user_id": "1dacdf00659111e594a3dea90594582e",
#       "user_type": 3,
#       "fingers": [
#         {
#           "id": "26e4d1cc55ee4dc5a02c0c61739cee71",
#           "value": "ywkPYqGqupRFR75wTW1CbKqbDHi7thR0l2wccLfmpJyr+dnxeGp7M33EAl8Cb15sOJrfY+msLHuj\ncAxRYa6kM3AZqGZK6smC90OfjOojn/T8hn6q7oizZjEw+mYHTHmdaZ+1Nq9atlYAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         },
#         {
#           "id": "33980497f37c4dbdb36a950b94583814",
#           "value": "ywkOXKGqmhTFxv5gze0CdKsbDHC7N5R4lW+cfLTg5ICoxbkJKItrV/REulUibvZuBJQUdGa4PCzZ\nEl8eDW60e0A4/UgP6Fn2g064Ahl+Lw7yvFySOtB9sG24vKi6XFoLWSm1NgAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         },
#         {
#           "id": "7bcd786293554724bd954507699fc297",
#           "value": "ywkPZKGqhZQ7RYGQMW56fGobzHQ6N5R4lW+cfLXgJICvxVgJ75uCTIhF33wwbZdD5ZxGRDS4rVgq\nUB9M6L6HxVIZngxDKe8I/sNZRHZmmcvThlzRyYXzTqURklxX/fzbFui1Nk6ytlYAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#         }
#       ]
#     }
#   ],
#   "supervisor_user_fingers": [
#    {
#      "user_name": "阿大",
#      "user_id": "0ed67e8061d311e5a016dea90594582e",
#      "user_type": 3,
#      "fingers": [
#        {
#          "id": "290e64a1ac024f3888b102cbeffa5c27",
#          "value": "ywkQSqGqhZQ7RZ6QTWxCTKuaDGi7thR0l2wccLfmJIyvyVgR76t/JGvE3kExbutLQJ7VqGGwF3ZE\nAHxww04fCsa4WiITqV9kecHZZFpkjsGMBt9s5MAfVBsDcQy0GXLzQpZlKDaKtlbw+Ld2AAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n"
#        }
#      ]
#    }
#   ],
#   "projects": [
#       {
#           "id": "01e65fe17d3211e586ccda932e028508",
#           "name": "123456"
#       }
#   ],
#   "version": 1,
#   "success": true
# }

def mfingers_project(req):
    dict = {}
    dict['version'] = 1
    dict['success'] = True
    dict['self_user_fingers'] = []
    dict['supervisor_user_fingers'] = []
    dict['projects'] = []

    try:
        if req.method == 'GET':
            rj = req.GET.get('data', '')
            rj = json.loads(rj)
            equipment_id = rj['equip_id']
            company_id = rj['company_id']

            cursor = connection.cursor()
            sql = 'SELECT * FROM view_finger WHERE user_type IN (3,4,5,6) AND company_id=\'' + company_id + '\''
            cursor.execute(sql)
            results = dictfetchall(cursor)

            user_fingers = {}
            for result in results:
                user_id = result['user_id']
                finger = {"id": result['id'], "value": result['finger_data']}

                if user_id in user_fingers.keys():
                    user_fingers[user_id]["fingers"].append(finger)
                else:
                    user_fingers[str(user_id)] = {
                        "user_name": result['user_name'],
                        "user_id": user_id,
                        "user_type": result['user_type'],
                        "fingers": [finger]
                    }

            for each in user_fingers:
                dict['self_user_fingers'].append(user_fingers[each])

            sql = 'SELECT * FROM view_finger WHERE is_supervisor=1 AND company_id=\'' + company_id + '\''
            cursor.execute(sql)
            results = dictfetchall(cursor)

            user_fingers = {}
            for result in results:
                user_id = result['user_id']
                finger = {"id": result['id'], "value": result['finger_data']}

                if user_id in user_fingers.keys():
                    user_fingers[user_id]["fingers"].append(finger)
                else:
                    user_fingers[str(user_id)] = {
                        "user_name": result['user_name'],
                        "user_id": user_id,
                        "user_type": result['user_type'],
                        "fingers": [finger]
                    }

            for each in user_fingers:
                dict['supervisor_user_fingers'].append(user_fingers[each])

            sql = 'SELECT id, name FROM app_project WHERE company_id=\'' + company_id + '\''
            cursor.execute(sql)
            dict['projects'] = dictfetchall(cursor)

    except:
        sys_info()
        dict['success'] = False

    return HttpResponse(json.dumps(dict))


# deleteUserFingerServerUri()
#     getServer1Address() + "/service/v1/scanner/burst_person/fingers";
# http delete
# http://182.92.190.30:9210/service/v1/scanner/burst_person/fingers/10d87cc0619611e58855dea90594582e
# user_id

def mfingers_delete(req, param):
    response = JsonResponse({'success': False}, safe=False)
    try:
        if req.method == 'DELETE':
            cursor = connection.cursor()
            sql = 'DELETE FROM app_finger WHERE user_id=\'' +param+ '\''
            cursor.execute(sql)
            return JsonResponse({"success": True}, safe=False)

        return response
    except:
        sys_info()
        return response


#data=%7B%22equip_id%22%3A%22861189014120793%22%2C%22items%22%3A%5B%7B%22project_blast_type_name%22%3A%22%E7%A1%90%E5%AE%A4%E7%88%86%E7%A0%B4%22%2C%22user_type%22%3A6%2C%22protected_obj_type_name%22%3A%22%E5%9C%9F%E7%AA%91%E6%B4%9E%22%2C%22protected_obj_type_id%22%3A1%2C%22protected_obj_distance%22%3A25%2C%22blast_area_name%22%3A%22%E4%B8%9C%E5%A4%A7%E7%88%86%E5%8C%BA1001%22%2C%22blast_transmission_v%22%3A23000%2C%22id%22%3A%22aea96fb12db34712afdc4018bc3969a3%22%2C%22user_name%22%3A%22%E7%88%86%E7%A0%B42%22%2C%22blast_shake_hz%22%3A54%2C%22blast_area_id%22%3A%226975d20d0d9f452aa65dd78af02e8a17%22%2C%22create_time%22%3A1493389028221%2C%22user_id%22%3A%22617465c74c62486bb40c0d10ae367b48%22%2C%22project_blast_type_id%22%3A1%7D%5D%7D
# {#
#    "items": [{
#        "id": "aea96fb12db34712afdc4018bc3969a3",
#        "blast_area_id": "6975d20d0d9f452aa65dd78af02e8a17",
#        "blast_area_name": "\u4e1c\u5927\u7206\u533a1001",
#        "user_id": "617465c74c62486bb40c0d10ae367b48",
#        "user_name": "\u7206\u78342",
#        "user_type": 6,
#        "protected_obj_type_id": 1,
#        "protected_obj_type_name": "土窑洞",
#        "project_blast_type_id": 1,
#        "project_blast_type_name": "硐室爆破",
#        "blast_shake_hz": 54,
#        "protected_obj_distance": 25,
#        "blast_transmission_v": 23000,
#        "create_time": 1493389028221,
#    }], "equip_id": "861189014120793"
# }

def mseismometer_record(req):
    response = JsonResponse({'success': False}, safe=False)
    try:
        if req.method == 'POST':
            rj = req.body.replace('data=', '')
            rj = urllib.unquote(rj)
            rj = json.loads(rj)
            items = rj['items']
            for item in items:
                record = Seismometer(
                    id=item['id'],
                    area=item['area'],
                    user=SysUser.objects.get(id=item['user']),
                    project_blast_type=ProjectBlastTypes.objects.get(id=item['project_blast_type_id']),
                    protected_obj_type=ProtectedObjectTypes.objects.get(id=item['protected_obj_type_id']),
                    protected_obj_distance=item['protected_obj_distance'],
                    blast_transmission_v=item['blast_transmission_v'],
                    blast_shake_hz=item['blast_shake_hz'],
                    create_time=strftime("%Y-%m-%d %H:%M:%S", localtime(item['create_time'] / 1000))
                )
                record.save()

            response = JsonResponse({"success": True}, safe=False)
            return response

        return response
    except:
        sys_info()
        return response

