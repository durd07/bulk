#!/usr/bin/python
import os

def update(bin):
    if not os.path.exists(bin):
        command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/build_park_960p/" + bin + " ."
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/build_vp_p/" + bin + " ."
        print(command)
        os.system(command)
    copy2device(ip, bin, "/tmp")
    run_cmd("/var/ftp/busybox sh /tmp/" + bin) 
    run_cmd("sync") 

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

for item in range(211, 212):
    ip = "192.168.1." + str(item)
    print("============ " + ip + " ============")
    update("PARK_20160125174403_A1.bin")
    run_cmd("/sbin/reboot -f &")
