#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import time
import getopt

def reminder():
    import send_mail
    print 'reminder'
    text = '''Hi All,
    泊车新版本将在今天晚上【21:00】开始编译，如有新的代码更新，请于今晚 21:00 前提交到svn。
    泊车新版本编译完成后，后将预定系统中没有预订的设备进行自动升级，如果某台设备需要保留旧版本，
    请在预订系统中将其预订。

    附：
    设备预订系统地址如下：
    http://192.168.1.164/mrbs/web/
    '''
    send_mail.send_mail(sub='[PARK BUILD REMINDER]',content=text)

def build():
    print 'build'
    # trigger jenkins build
    global version
    global pack_name
    global pack_url
    global pack_url1
    version = time.strftime('PARK_A04_01_%Y%m%dA1',time.localtime(time.time()))
    pack_name = version + ".bin"
    pack_name_full = version + "_full.bin"

    pack_url = "http://192.168.1.164:7856/jenkins/park/release/bin/" + pack_name;
    pack_url1 = "http://192.168.1.164:7856/jenkins/park/release/bin/" + pack_name_full;

    #os.system("java -jar /home/durd/test/jenkins-cli.jar -s http://192.168.1.164:8080/ build PARK -s -v -p VERSION=" + version)
    #os.system("cd /home/durd/dm8127/jenkins/park/release/bin && git add " + pack_name + "&& git commit " + " -m \"add new park version " + pack_name + "\"")
    #os.system("cd /home/durd/dm8127/jenkins/park/release/bin && git add " + pack_name_full + "&& git commit " + " -m \"add new park version " + pack_name_full + "\"" + "&& git svn rebase && git svn dcommit")

    ship2device()

ip_except=['192.168.1.212']
ip_list=[]
def ship2device():
    from mysql_handler import get_except_ip
    global ip_except
    ip_except = get_except_ip()
    print ip_except

    for item in range(211, 212):
        ip = '192.168.1.' + str(item)
        global ip_except
        if ip in ip_except:
            print 'ip is except'
        else:
            global ip_list
            ip_list.append(ip)
            print ip
            print pack_name
            from run_cmd import update
            update(ip, pack_name)

    time.sleep(120)

    global pack_url
    global pack_url1
    text = 'HI ALL, \n泊车版本已经打包完成, 你可以在如下地址获取到最新的泊车版本\n' + pack_url + '\n' + pack_url1
    text = text + "\n\n更新内容可在http://192.168.1.164:8080/job/PARK/lastBuild/changes 获得.\n\n"
    text = text + "\n\n目前如下设备已经升级到最新版本([X]代表已升级， [ ]代表未升级)：\n\n"

    from run_cmd import run_cmd
    for item in range(211, 212):
        ip = '192.168.1.' + str(item)
        version_text = run_cmd(ip, 'cat /var/version/version')
        v = version_text.split('=')
        version_text = v[1]
        global version
        if ip in ip_except:
            text = text + '[ ] ' + ip + '\n'
        else:
            text = text + '[X] ' + ip + '      ' + version_text + '\n'

    import send_mail
    send_mail.send_mail(sub="[PARK BUILD FINISHED] " + pack_name, content=text)

def usage():
    return sys.argv[0] + '\nreminder send the reminder email.\nbuild build.\n'

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'rb', ['reminder', 'build'])
    except getopt.GetoptError as err:
        print usage()
        sys.exit(2)

    for opt, arg in opts:
        print usage()
        sys.exit()

    for arg in args:
        if arg in ('reminder'):
            reminder()
            sys.exit()
        elif arg in ('build'):
            build()
            sys.exit()
        else:
            assert False, 'unhandled option'

if __name__ == '__main__':
    main(sys.argv[1:])
