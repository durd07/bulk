#!/usr/bin/env python
#-*- coding: utf-8 -*-

import smtplib
import email.mime.multipart
import email.mime.text
from email.mime.text import MIMEText
#mailto_list=["durd_bitcom@163.com",
#             "guofulei_bitcom@163.com",
#             "zhongmh_bitcom@163.com",
#             "zhengweixue_bitcom@163.com",
#             "guofeifei_bitcom@163.com",
#             "chenyajun_bitcom@163.com",
#             "liuqin_bitcom@163.com",
#             "futingjie_bitcom@163.com",
#             "weifang_bitcom@163.com",
#             "suimeiji_bitcom@163.com"]
mailto_list=["durd_bitcom@163.com"]

mail_host="smtp.163.com"  #设置服务器
mail_user="durd_bitcom"    #用户名
mail_pass="bitcom2016"   #口令
mail_postfix="163.com"  #发件箱的后缀

def send_mail(sub, content, to_list=mailto_list):  #to_list：收件人；sub：主题；content：邮件内容
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
