#!/usr/bin/python3
import os
import http.client

def update(bin):
    if not os.path.exists(bin):
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/release/build_park_960p/" + bin + " ."
        command = "cp /home/durd/work/build/" + bin + " ."
        print(command)
        os.system(command)
    copy2device(bin, "/tmp")
    run_cmd("/var/ftp/busybox sh /tmp/" + bin) 
    run_cmd("sync") 

def httpget(cmd):
    conn = http.client.HTTPConnection(ip, 80)
    conn.request("GET", "/index.htm")
    result = conn.getresponse()
    print(result.status, result.reason)

    data = result.read()
    print(data)
    conn.close()

def httpcfg(cmd):
    conn = http.client.HTTPConnection(ip, 80)
    conn.request("GET", "/vb.htm?" + cmd)
    result = conn.getresponse()
    print(result.status, result.reason)

    data = result.read()
    print(data)
    conn.close()

def run_cmd(cmd):
    #command = "ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no bit1@" + ip + " \"" + cmd + "\""
    command = "ssh bit1@" + ip + " \"" + cmd + "\""
    #print(command)
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
#for item in [112, 114, 116]:
    ip = "192.168.1." + str(item)
    print("\033[95m============ " + ip + " ============\033[0m")
    try:
        #httpcfg("timefrequency=-1&datestampenable3=2&sntpip=58.58.40.162")
        #httpcfg("pt_set_save=4,1,0,58.58.40.162,10000,20000,58.58.40.162,18901,3702")
        #httpcfg("network_card_type=4")
        #run_cmd(r"sed -i '1i\ETHTOOL_OPTS=\"speed 10 duplex half autoneg off\"' /mnt/nand/info.cfg")
        #run_cmd("cat /mnt/nand/info.cfg | grep ETH | wc")
        #copy2device("/home/durd/work/ipnc_rdk/target/filesys/opt/ipnc/vd", "/tmp/vd")
        copy2device("/home/durd/work/ipnc_rdk/ipnc_app/vd/build/vd", "/tmp/vd")
        run_cmd("mv /tmp/vd /opt/ipnc/")
        #run_cmd("/opt/ipnc/pid_status  -q|awk \'NR>4&&(\$6>120||\$8>100) {print  \$4 \\\"\\t\\\" \$6 \\\"\\t\\\" \$8 \\\"\\t\\\" \$9 }\' ")
        #run_cmd("/opt/ipnc/pid_status  -q|awk \'{print  \$4 \\\"\\t\\\" \$6 \\\"\\t\\\" \$8 \\\"\\t\\\" \$9 }\' ")
        #run_cmd("uptime")
        #run_cmd("date")
        #run_cmd("killall -9 vd")
        #run_cmd("tail -f /tmp/log/vd.log")
        #run_cmd("sync ; /sbin/reboot -f &")
        #update("PARK_20160302161421_A1.bin")
        #run_cmd("/sbin/reboot -f &")
    except Exception as e:
        print("\033[91m" + ip + " !!!FAILED!!!" + "\033[0m", "\033[93m", e, "\033[0m")
        continue

"""
Pre defined actions
1.  set ntp server 
    httpcfg("timefrequency=-1&datestampenable3=2&sntpip=58.58.40.162")
"""
