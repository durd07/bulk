#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
mailto_list=["durd_bitcom@163.com",
             "guofulei_bitcom@163.com",
             "zhongmh_bitcom@163.com",
             "zhengweixue_bitcom@163.com",
             "guofeifei_bitcom@163.com",
             "chenyajun_bitcom@163.com",
             "liuqin_bitcom@163.com",
             "futingjie_bitcom@163.com",
             "weifang_bitcom@163.com",
             "suimeiji_bitcom@163.com"]

mail_host="smtp.163.com"  #设置服务器
mail_user="durd_bitcom"    #用户名
mail_pass="bitcom2016"   #口令
mail_postfix="163.com"  #发件箱的后缀

def run_cmd(cmd):
    command = "ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no bit1@" + ip + " \"" + cmd + "\""
    #command = "ssh bit1@" + ip + " \"" + cmd + "\""
    #print(command)
    os.system(command)

def copy2device(from_path, to_path):
    command = "scp -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no " + from_path + " bit1@" + ip + ":" + to_path
    print(command)
    os.system(command)

def update(bin):
    if not os.path.exists(bin):
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/release/build_park_960p/" + bin + " ."
        command = "cp /home/durd/dm8127/jenkins/park/release/bin/" + bin + " ."
        print(command)
        os.system(command)
    copy2device(bin, "/tmp")
    run_cmd("/var/ftp/busybox sh /tmp/" + bin)
    run_cmd("sync")
    run_cmd("/sbin/reboot -f &")

def send_mail(to_list, sub, content):  #to_list：收件人；sub：主题；content：邮件内容
    me="DURD"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = email.mime.multipart.MIMEMultipart()
    txt = MIMEText(content, _charset='utf8')    #创建一个实例，这里设置为html格式邮件
    msg.attach(txt)
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False


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

import time
ip_list = []
ip_except = []
if __name__ == '__main__':
    if sys.argv[1] == "reminder":

        text = '''Hi All,
        泊车新版本将在今天晚上【21:00】开始编译，如有新的代码更新，请于今晚 21:00 前提交到svn。
        泊车新版本编译完成后，后将预定系统中没有预订的设备进行自动升级，如果某台设备需要保留旧版本，
        请在预订系统中将其预订。

        附：
        设备预订系统地址如下：
        http://192.168.1.164/mrbs/web/
        '''
        send_mail(mailto_list,"[PARK BUILD REMINDER]",text)

    elif sys.argv[1] == "build":
        # trigger jenkins build
        version = time.strftime('PARK_A04_01_%Y%m%dA1',time.localtime(time.time()))
        pack_name = version + ".bin"
        pack_name_full = version + "_full.bin"
        pack_url = "http://192.168.1.164:7856/jenkins/park/release/bin/" + pack_name;
        pack_url1 = "http://192.168.1.164:7856/jenkins/park/release/bin/" + pack_name_full;
        os.system("java -jar /home/durd/test/jenkins-cli.jar -s http://192.168.1.164:8080/ build PARK -s -v -p VERSION=" + version)
        os.system("cd /home/durd/dm8127/jenkins/park/release/bin && git add " + pack_name + "&& git commit " + " -m \"add new park version " + pack_name + "\"")
        os.system("cd /home/durd/dm8127/jenkins/park/release/bin && git add " + pack_name_full + "&& git commit " + " -m \"add new park version " + pack_name_full + "\"" + "&& git svn rebase && git svn dcommit")
        global ip_except
        ip_except = get_except_ip()
        print ip_except

        for item in range(211, 237):
            ip = '192.168.1.' + str(item)
            if ip in ip_except:
                print 'ip is except'
            else:
                global ip_list
                ip_list.append(ip)
                print ip
                print pack_name
                update(pack_name)


        text = 'HI ALL, \n泊车版本已经打包完成, 你可以在如下地址获取到最新的泊车版本\n' + pack_url + '\n' + pack_url1
        text = text + "\n\n更新内容可在http://192.168.1.164:8080/job/PARK/lastBuild/changes 获得.\n\n"
        text = text + "\n\n目前如下设备已经升级到最新版本([X]代表已升级， [ ]代表未升级)：\n\n"
        for item in range(211, 237):
           ip = '192.168.1.' + str(item)
           if ip in ip_except:
               text = text + '[ ] ' + ip + '\n'
           else:
               text = text + '[X] ' + ip + '\n'

        send_mail(mailto_list,"[PARK BUILD FINISHED] " + pack_name,text)
