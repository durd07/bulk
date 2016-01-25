#!/usr/bin/python
import os

def update(bin):
    if not os.path.exists(bin):
        command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/build_park_960p/" + bin + " ."
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/build_vp_p/" + bin + " ."
        print(command)
        os.system(command)
    copy2device(ip, bin, "/tmp")
    run_cmd(ip, "/var/ftp/busybox sh /tmp/" + bin) 
    run_cmd(ip, "sync") 

def run_cmd(ip, cmd):
    command = "ssh bit1@" + ip + " \"" + cmd + "\""
    print(command)
    os.system(command)

def copy2device(ip, from_path, to_path):
    command = "scp " + from_path + " bit1@" + ip + ":" + to_path
    print(command)
    os.system(command)

def copyfromdevice(ip, from_path, to_path):
    command = "scp " + "bit1@" + ip + ":" + from_path + " " + to_path
    print(command)
    os.system(command)

for item in range(101, 139):
    ip = "192.168.1." + str(item)
    dev_num = "3702020" + str(item)
    jiekou_num = "3702020000507" + str(item)
    park_num = "370202010" + str(item)
    print("============ " + ip + " = " + dev_num + " = " + jiekou_num + " = " + park_num)
    run_cmd(ip, "sed -i 's/<device_id>.*<\/device_id>/<device_id>" + dev_num + "<\/device_id>/g' /config/arm_config.xml")
    run_cmd(ip, "sed -i 's/<deviceID>.*<\/deviceID>/<deviceID>" + dev_num + "<\/deviceID>/g' /config/dsp_config.xml")
    run_cmd(ip, "sed -i 's/Net_DeviceID=.*/Net_DeviceID=" + dev_num + ";/g' /config/message.txt")


    run_cmd(ip, "sed -i 's/<exp_device_id>.*<\/exp_device_id>/<exp_device_id>" + jiekou_num + "<\/exp_device_id>/g' /config/arm_config.xml")

    run_cmd(ip, "sed -i 's/<spot_id>.*<\/spot_id>/<spot_id>" + park_num + "<\/spot_id>/g' /config/arm_config.xml")
    run_cmd(ip, "sed -i 's/<spotID>.*<\/spotID>/<spotID>" + park_num + "<\/spotID>/g' /config/dsp_config.xml")

    run_cmd(ip, "/sbin/reboot -f &")
