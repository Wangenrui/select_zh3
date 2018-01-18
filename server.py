#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import MySQLdb
import SocketServer
import traceback
import copy


def getXor(str):
    a = 0
    for b in bytearray(str):
        a ^= b
    return a


class MyTCPHandler(SocketServer.StreamRequestHandler):
    true = '#06O106$' # message for correct package
    false = '#06R119$' # message for correct package

    def dictfetchall(self, cursor):
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
            ]

    def process(self, list):
        print list
        try:
            print 'start save'
            conn = MySQLdb.connect(host=DB_HOST, user=USER, passwd=PASSWORD, port=DB_PORT, charset='utf8')
            cur = conn.cursor()
            conn.select_db(INSTANCE)

            sql = '''
                SELECT a.id AS equipment_id, equipment_code, b.id AS area_id, b.apply_user_id AS user_id
                    FROM app_equipment a
                    LEFT JOIN app_area b ON b.equipment_id=a.id
                    WHERE a.equipment_code=%s
            '''
            cur.execute(sql, [list[0]['equipment_code']])
            ret = self.dictfetchall(cur)[0]
            print ret

            for item in list:
                value = [
                    item['longitude'],
                    item['latitude'],
                    item['blast_time'],
                    item['code'],
                    item['company_code'],
                    item['special_code'],
                    item['serial_code'],
                    item['status_id'],
                    item['manu_date'],
                    ret['area_id'],
                    ret['equipment_id'],
                    ret['user_id'],
                    datetime.datetime.now()
                ]

                sql = '''
                    SELECT COUNT(*) AS count FROM app_digitaldetonator a WHERE a.code=%s
                '''
                cur.execute(sql, [value[3]])
                count = self.dictfetchall(cur)[0]

                if int(count['count']) != 0:
                    sql = '''
                        UPDATE app_digitaldetonator a
                        SET longitude=%s, latitude=%s, blast_time=%s, code=%s, company_code=%s, special_code=%s,
                            serial_code=%s, status_id=%s, manu_date=%s, area_id=%s, equipment_id=%s, user_id=%s, create_time=%s
                        WHERE a.code=%s
                    '''
                    value.append(value[3])
                else:
                    sql = '''
                        INSERT INTO app_digitaldetonator
                        (longitude, latitude, blast_time, code, company_code, special_code,
                        serial_code, status_id, manu_date, area_id, equipment_id, user_id, create_time)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
                cur.execute(sql, value)

            conn.commit()
            cur.close()
            conn.close()
            print 'save success'

        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def checkOne(self, data):
        l = len(data)
        if data[0] != '*' or data[len(data)-1] != '$': # check head '*' and tail '$'
            return False

        if int(data[5:8]) != l: # check length
            return False

        if int(data[l-4:l-1]) != getXor(data[0:l-4]):  # check XOR
            return False

        return True


    def handle(self):
        # self.request is the TCP socket connected to the client
        # Ex1:
        #   *0201048571700351040830306290170528093242001017$*020203457170035000000Z037D74E115$
        # Ex2:
        #   *0301048571700490000000000000170429174529074027$*030298657170049000000Z8A6766O000000Z8A654FO000000Z89C02BO000000Z8AA69EO000000Z8A13DFO000000Z8A11EAO000000Z8A121EO000000Z8A4FD0O000000Z8AAD88O000000Z8AAC13O000000Z8AAC50O000000Z89C150O000000Z8AAC47O000000Z85C112O000000Z85B459O000000Z85C1C6O000000Z8A8593O000000Z8AF691O000000Z8AE9C2O000000Z8A84B4O000000Z8A19B3O000000Z8A1AB3O000000Z89D8F7O000000Z89D02AO000000Z89CFFAO000000Z85C1FAO000000Z85C269O000000Z85BF59O000000Z8AAC02O000000Z8AAAD1O000000Z8AA9FDO000000Z89F4E3O000000Z89BAFFO000000Z8AAB05O000000Z89D503O000000Z89D71AO000000Z8A4EE3O000000Z8A9131O000000Z89BF89O000000Z8AABE1O000000Z8AAC6AO000000Z8A6A20O000000Z89C301O000000Z8A6668O000000Z89BF59O000000Z89C315O000000Z8A6A52O000000Z8AADDCE000000Z8A86D8O000000Z8A1550O000000Z85BFC3O000000Z85C1E9O000000Z8A8CEAO000000Z89FF96O000000Z89FB3BO000000Z89FCF4O000000Z8A1CAAO000000Z8A1AE3O000000Z8A197FO000000Z89FD24O000000Z8A8BEBO000000Z89C4B5O000000Z8A836FO000000Z8AAC00O000000Z85BE80O000000Z85C09FO000000Z85BEB2O000000Z85C14DO000000Z85B809O011$
        #   *030309057170049000000Z860F28O000000Z85C5F0O000000Z8A9258O000000Z8A90FDO000000Z03dd75E118$
        # Ex3:
        #   *0201048571700311047635314952170527113241008019$
        #   *0202132571700312970318L00001O2970318L00004O2970318L00002O2970318L00005O2970318L00003O2970318L00000O2970318L00006O2970318L00007O028$

        print 'handle'
        return_message = True
        list = []
        dict = {}

        while True: # handle multimessage in one connection
            try:
                self.data = self.request.recv(16384).strip()
                print "{} wrote:".format(self.client_address[0])
                if len(self.data) == 0:
                    print 'connection is closed by client'
                    break

                print str(len(self.data)) +' bytes: '+ self.data

                lenth = int(self.data[1:3])
                index = int(self.data[3:5])
                print 'get #' + str(index) +' of total '+ str(lenth)

                return_message *= self.checkOne(self.data)

                if index == 1:
                    dict['equipment_code'] = self.data[8:16]
                    dict['longitude'] = self.data[16:19] + '.' + self.data[19:23]
                    dict['latitude'] = self.data[23:25] +'.'+ self.data[25:29]
                    dict['blast_time'] = self.data[29:31] +'-'+ self.data[31:33] +'-'+ self.data[33:35] +' '+ \
                        self.data[35:37] +':'+ self.data[37:39] +':'+ self.data[39:41]
                    print dict

                else:
                    count = (int(self.data[5:8]) - 8) / 14  # detonator count
                    print 'detonator count: ' + str(count)

                    for j in range(0, count):
                        s = 14*j + 16
                        status = self.data[(s+13):(s+14)]
                        if status == 'O':
                            dict['status_id'] = 0
                        elif status == 'E':
                            dict['status_id'] = 1
                        else:
                            return_message *= False
                            break

                        code = self.data[s:(s+13)]
                        dict['code'] = code
                        dict['company_code'] = code[0:2]
                        dict['special_code'] = code[7:8]
                        dict['serial_code'] = code[8:13]
                        year = str(datetime.datetime.now().year)
                        dict['manu_date'] = year[2:3] + code[2:3] + '-' + code[3:5] + '-' + code[5:7]
                        list.append(copy.deepcopy(dict))

                if index == lenth:
                    if return_message:
                        print self.true
                        self.request.sendall(self.true)
                    else:
                        print self.false
                        self.request.sendall(self.false)

            except:
                traceback.print_exc()
                break

        self.process(list)

        print 'end of handle'


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8002
    DB_HOST, DB_PORT = "127.0.0.1", 3306
    USER, PASSWORD = "root", "password"
    INSTANCE = "select_zh1"

    # Create the server, binding to localhost on port 9999
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you interrupt the program with Ctrl-C
    server.serve_forever(poll_interval=10)
