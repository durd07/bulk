#!/usr/bin/python3
import os
import time
import subprocess
import http.client
import threading

output_list = {} 
def update(bin):
    if not os.path.exists(bin):
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/release/build_park_960p/" + bin + " ."
        command = "cp /home/durd/work/build/" + bin + " ."
        #print(command)
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
    command = "ssh tzhtc@" + ip + " \"" + cmd + "\""
    #print(command)
    os.system(command)

def run_cmd_concurrent(ip, cmd):
    command = "ssh tzhtc@" + ip + " \"" + cmd + "\""
    #print(command)
    outs = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    #proc = subprocess.Popen(command, shell=True)
    #try:
    #    outs, errs = proc.communicate(timeout=60) 
    global output_list
    output_list[ip] = outs
    #print(output_list[ip])
    #except TimeoutExpired:
    #    proc.kill()
    #    outs, errs = proc.communicate()

    

def copy2device(from_path, to_path):
    command = "scp " + from_path + " bit1@" + ip + ":" + to_path
    print(command)
    os.system(command)

def copyfromdevice(from_path, to_path):
    command = "scp " + "bit1@" + ip + ":" + from_path + " " + to_path
    print(command)
    os.system(command)

#for item in range(211, 237):
for item in [161,162,163,165,166,171,172,173,177,178]:
    #ip = "192.168.8.8"
    ip = "10.121.1." + str(item)
    #global output_list
    output_list[ip] = ip 
    #print("\033[95m============ " + ip + " ============\033[0m")
    #print("\n@@@@@@@@@@@@@@@@ " + ip + " @@@@@@@@@@@@@@@@")
    try:
#echo "------ $ip -- `ssh root@$ip "hostname"` ------"
        t1 = threading.Thread(target=run_cmd_concurrent, args=(ip, "echo ----------------------------- \`hostname\` -------------------------------- && date && ntpq -p", ))
        t1.start()
        #run_cmd_concurrent("echo ----------------------------- \`hostname\` -------------------------------- && date && ntpq -p")
        #run_cmd_concurrent("ntpq -p")
        #run_cmd("hostname")
        #httpcfg("timefrequency=-1&datestampenable3=2&sntpip=202.112.7.13")
        #httpcfg("pt_set_save=4,1,0,58.58.40.162,10000,20000,58.58.40.162,18901,3702")
        #httpcfg("network_card_type=4")
        #run_cmd(r"sed -i '1i\ETHTOOL_OPTS=\"speed 10 duplex half autoneg off\"' /mnt/nand/info.cfg")
        #run_cmd("cat /mnt/nand/platform_set.cfg")
        #copy2device("/home/durd/work/ipnc_rdk/ipnc_app/vd/build/vd", "/tmp/vd")
        #run_cmd("mv /tmp/vd /opt/ipnc/vd")
        #copy2device("/home/durd/work/ipnc_rdk/target/filesys/opt/ipnc/firmware/ipnc_rdk_fw_m3vpss.xem3", "/tmp/ipnc_rdk_fw_m3vpss.xem3")
        #copy2device("/home/durd/repo/bulk/preview.htm", "/var/www/preview.htm")
        #run_cmd("mv /tmp/ipnc_rdk_fw_m3vpss.xem3 /opt/ipnc/firmware/ipnc_rdk_fw_m3vpss.xem3")
        #copy2device("platform_set.cfg", "/mnt/nand")
        #copy2device("/home/durd/test/package/lrzsz-0.12.20/src/rz", "/usr/bin")
        #copy2device("/home/durd/test/package/lrzsz-0.12.20/src/sz", "/usr/bin")
        #run_cmd("cat /var/version/version")
        #run_cmd("rm -rf /home/records/*")
        #run_cmd("sync && /sbin/reboot -f &")
        #os.system("ping " + ip)
        #run_cmd("/opt/ipnc/pid_status  -q|awk \'NR>4&&(\$6>120||\$8>100) {print  \$4 \\\"\\t\\\" \$6 \\\"\\t\\\" \$8 \\\"\\t\\\" \$9 }\' ")
        #run_cmd("/opt/ipnc/pid_status  -q|awk \'{print  \$4 \\\"\\t\\\" \$6 \\\"\\t\\\" \$8 \\\"\\t\\\" \$9 }\' ")
        #run_cmd("uptime")
        #run_cmd("cat /var/version/version")
        #run_cmd("killall -9 vd")
        #run_cmd("tail -f /tmp/log/vd.log")
        #copy2device("platform_set.cfg", "/mnt/nand/platform_set.cfg")
        #update("PARK_A04_01_20160413192728_A1.bin")
        #run_cmd("rm -rf /home/records/*")
        #run_cmd("killall -9 vd &")
        #run_cmd("cat /var/version/version")
    except Exception as e:
        print("\033[91m" + ip + " !!!FAILED!!!" + "\033[0m", "\033[93m", e, "\033[0m")
        continue

time.sleep(5)
for item in [161,162,163,165,166,171,172,173,177,178]:
    #ip = "192.168.8.8"
    ip = "10.121.1." + str(item)
    #global output_list
    print(output_list[ip].decode('utf-8'))
"""
Pre defined actions
1.  set ntp server
    httpcfg("timefrequency=-1&datestampenable3=2&sntpip=58.58.40.162")
2.  set platform for zehin
    httpcfg("pt_set_save=4,1,0,58.58.40.162,10000,20000,58.58.40.162,18901,3702")
"""
