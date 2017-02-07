#!/usr/bin/python3
# -*- codeing: utf-8 -*-

'''
ssh to each device and cat /var/version/version
the command run concurrently.
'''

import os
import http.client
import subprocess
import time
import csv
import logging
import logging.handlers
import concurrent.futures

class Node():
    def __init__(self, space_code, ip):
        self.space_code = space_code
        self.ip = ip

def update(ip, bin):
    outs = ''
    if not os.path.exists(bin):
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/release/build_park_960p/" + bin + " ."
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/jenkins/park/release/bin/" + bin + " ."
        command = "cp /home/durd/work/build/" + bin + " ."
        print(command)
        os.system(ip, command)
    outs += copy2device(ip, bin, "/var/ftp")
    #outs += run_cmd(ip, "/var/ftp/busybox sh /tmp/" + bin)
    outs += run_cmd(ip, "/var/ftp/updatatraffic.sh " + bin)
    outs += run_cmd(ip, "sync")
    outs += run_cmd(ip, "sync")
    return outs

def httpget(ip, cmd):
    conn = http.client.HTTPConnection(ip, 80)
    conn.request("GET", "/index.htm")
    result = conn.getresponse()
    print(result.status, result.reason)

    data = result.read()
    print(data)
    conn.close()

def httpcfg(ip, cmd):
    try:
        conn = http.client.HTTPConnection(ip, 80, timeout=10)
        conn.request("GET", "/vb.htm?" + cmd)
        result = conn.getresponse()
        print(result.status, result.reason)
        data = result.read()
        print(data)
        conn.close()
    except Exception as e:
        logger.error('%s %s failed. %s' % (ip, cmd, e))

def run_cmd(ip, cmd):
    #command = "ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no bit1@" + ip + " \"" + cmd + "\""
    command = "ssh bit1@" + ip + " \"" + cmd + "\""
    #print(command)
    #os.system(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    try:
        outs, errs = p.communicate(timeout=10)
    except subprocess.TimeoutExpired as e:
        p.kill()
        outs, errs = p.communicate()
        logger.error('%s %s failed. %s' % (ip, cmd, e))
        print('%s %s failed. %s' % (ip, cmd, e))
    except Exception as e:
        logger.error('%s %s failed. %s' % (ip, cmd, e))
        print('%s %s failed. %s' % (ip, cmd, e))
    finally:
        return outs.decode()

def run_cmd_concurrent(cmd):
    command = "ssh tzhtc@" + ip + " \"" + cmd + "\""
    subprocess.call(cmd, shell=True)

def copy2device(ip, from_path, to_path):
    command = "scp " + from_path + " bit1@" + ip + ":" + to_path
    os.system(command)
    return command

def copyfromdevice(ip, from_path, to_path):
    command = "scp " + "bit1@" + ip + ":" + from_path + " " + to_path
    print(command)
    os.system(command)

#def do_action(space_code, ip):
#    try:
#        print("\033[95m============ " + ip + " ===== " + space_code + "=======\033[0m")
#        run_cmd(ip, "grep 10122 /config/dsp_config.xml")
#        update(ip, "PARK_cs_20161228131251_A1.bin")
#        httpcfg(ip, r"timefrequency=-1&datestampenable3=2&sntpip=192.168.80.76")
#        run_cmd(ip, r"sed -i 's/<spot_id>.*<\/spot_id>/<spot_id>" + space_code + "<\/spot_id>/' /config/arm_config.xml")
#        run_cmd(ip, r"sed -i 's/<spotID>.*<\/spotID>/<spotID>" + space_code + "<\/spotID>/' /config/dsp_config.xml")
#        run_cmd(ip, r"rm -rf /home/records/* && sync && /sbin/reboot -f &")
#    except Exception as e:
#        print("\033[91m" + ip + " !!!FAILED!!!" + "\033[0m", "\033[93m", e, "\033[0m")
#        continue

def log_init():
    global logger
    LOG_FILE = 'ping.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 20*1024*1024, backupCount = 100)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger('test')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def do_action(space_code, ip):
    try:
        outs = ''
        outs += run_cmd(ip, r"cat /var/version/version")
        return outs
    except Exception as e:
        #print("\033[91m" + ip + " !!!FAILED!!!" + "\033[0m", "\033[93m", e, "\033[0m")
        logger.error('%s %s %s' % (space_code, ip, e))
        print('%s %s %s' % (space_code, ip, e))
        return ''

def do_action_concurrent(nodes):
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        # Start the load operations and mark each future with its command
        future_action = {executor.submit(do_action, node.space_code, node.ip): node for node in nodes}
        for future in concurrent.futures.as_completed(future_action):
            item = future_action[future]
            try:
                result = future.result()
                logger.info('===== %s %s =====\n%s' % (item.space_code, item.ip, result))
            except Exception as e:
                logger.error('%s %s %s' % item.space_code, item.ip, e)

def main():
    global logger
    log_init()

    nodes = []
    with open('ip.csv', newline='') as csvfile:
        ip_list = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in ip_list:
            if row[0].startswith('#'):
                continue
            [space_code, ip] = row
            node = Node(space_code, ip)
            nodes.append(node)

    do_action_concurrent(nodes)

if __name__ == '__main__':
    main()

"""
Pre defined actions
1.  set ntp server
    httpcfg("timefrequency=-1&datestampenable3=2&sntpip=58.58.40.162")
2.  set platform for zehin
    httpcfg("pt_set_save=4,1,0,58.58.40.162,10000,20000,58.58.40.162,18901,3702")
"""
