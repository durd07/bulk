#!/usr/bin/env python
#-*- coding: utf-8 -*-

import MySQLdb

def get_except_ip():
    try:
        ip_except = []
        conn=MySQLdb.connect(host='localhost',user='root',passwd='bitcom',db='mrbs',port=3306)
        cur=conn.cursor()
        cur.execute('SELECT * FROM `mrbs_entry`  where sysdate() between FROM_UNIXTIME(start_time) and FROM_UNIXTIME(end_time)')
        results = cur.fetchall()
        for row in results:
            room_id = row[5]
            cur.execute('select room_name from `mrbs_room` where id = ' + str(room_id))
            results = cur.fetchall()
            ip_except.append(results[0][0])
        cur.close()
        conn.close()
        return ip_except
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
