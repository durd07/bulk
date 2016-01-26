#!/usr/bin/python
import os
import httplib

def update(bin):
    if not os.path.exists(bin):
        command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/build_park_960p/" + bin + " ."
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/build_vp_p/" + bin + " ."
        print(command)
        os.system(command)
    copy2device(bin, "/tmp")
    run_cmd("/var/ftp/busybox sh /tmp/" + bin) 
    run_cmd("sync") 

def http(cmd):
    conn = httplib.HTTPConnection(ip, 80)
    conn.request("GET", "/index.htm")
    result = conn.getresponse()
    print(result.status, result.reason)

    data = result.read()
    print(data)
    conn.close()

def httpcfg(cmd):
    conn = httplib.HTTPConnection(ip, 80)
    conn.request("GET", "/vb.htm?" + cmd)
    result = conn.getresponse()
    print(result.status, result.reason)

    data = result.read()
    print(data)
    conn.close()

def run_cmd(cmd):
    command = "ssh bit1@" + ip + " \"" + cmd + "\""
    print(command)
    os.system(command)

def copy2device(from_path, to_path):
    command = "scp " + from_path + " bit1@" + ip + ":" + to_path
    print(command)
    os.system(command)

def copyfromdevice(from_path, to_path):
    command = "scp " + "bit1@" + ip + ":" + from_path + " " + to_path
    print(command)
    os.system(command)

for item in range(212, 237):
    ip = "192.168.1." + str(item)
    print("============ " + ip + " ============")
    httpcfg("timefrequency=-1&datestampenable3=2&sntpip=202.112.7.13&ntpinterval=30")
