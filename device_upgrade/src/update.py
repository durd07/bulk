#!/usr/bin/python3

import re
import os
import time
import urllib
import configuration
from utils import RunCommand
from utils import HttpUtil

class DeviceUpgrade():
    '''the main class for process.'''
    def __init__(self):
        self.ssh = RunCommand()
        self.conf = configuration.device_configuration()

    def upgrade(self, firmware):
        if not os.path.exists(firmware):
            ##################################################
            cmd = 'scp durd@192.168.1.164:/home/durd/dm8127/jenkins/park/release/bin/'\
                + firmware + ' .'
            os.system(cmd)

        self.ssh.do_scp_put(firmware, '/tmp/' + firmware)
        self.ssh.do_run('/var/ftp/busybox sh ' + '/tmp/' + firmware)

    def install_openvpn(self, client_key, client_crt, firmware=''):
        if firmware == '':
            self.upgrade('openvpn_patch_20160426113637_A1.bin')
        else:
            self.upgrade('openvpn_patch_20160426113637_A1.bin')

        self.ssh.do_scp_put(client_key, '/opt/ipnc/openvpn/client.key')
        self.ssh.do_scp_put(client_crt, '/opt/ipnc/openvpn/client.crt')
        for host in self.ssh.hosts:
            HttpUtil.httpget(host[0], '/cgi-bin/net_adv.cgi?openvpn_enable=1')

    def set_ntp(self, ntp_server, ntp_interval, ntp_type):
        for host in self.ssh.hosts:
            HttpUtil.httpcfg(host[0],
                             'language=ie&datestampenable3=' + str(ntp_type) +
                             '&sntpip=' + ntp_server +
                             '&ntpinterval=' + str(ntp_interval))

    def space_code_provision(self, new_space_code):
        r = '''/vb.htm?IntelligentInfo={"version":1.1,"method":"get","devicetype":1}'''
        for host in self.ssh.hosts:
            data = HttpUtil.httpget(host[0], r)
            json = data.split(' ')[-1]
            print('get intelligentinfo = %s' % json)
            output = re.sub('''"pointcode":"[0-9]*''',
                            '''"pointcode":"''' + new_space_code,
                            json)
            newdata = '/vb.htm?language=ie&IntelligentInfo=' + urllib.parse.quote(output)
            HttpUtil.httpget(host[0], newdata)

    def reboot(self):
        self.ssh.do_run('sync && /sbin/reboot -f &')
        time.sleep(10)

        for x in range(20):
            if self.ssh.do_probe((self.conf.ip,
                                  self.conf.user,
                                  self.conf.passwd)):
                return True;
            time.sleep(3)
        return False

    def run(self):
        for x in range(20):
            if self.ssh.do_probe(self.conf.ip + ',' +
                                 self.conf.user + ',' +
                                 self.conf.passwd):
                break;
            time.sleep(3)

        self.ssh.do_add_host(self.conf.ip + ',' +
                             self.conf.user + ',' +
                             self.conf.passwd)
        self.ssh.do_connect()
        print('connect to %s successfully.' % self.conf.ip)

        if self.conf.firmware_update:
            print('updateing to new firmware %s' % self.conf.new_firmware_version)
            self.upgrade(self.conf.new_firmware_version)

        if self.conf.update_time_config:
            print('setting up ntp server')
            self.set_ntp(self.conf.new_ntp_server,
                         self.conf.new_ntp_interval,
                         self.conf.new_ntp_type)

        if self.conf.enable_openvpn:
            print('installing openvpn')
            self.install_openvpn(self.conf.client_key_path,
                            self.conf.client_crt_path)

        #if self.conf.provision_space_code:
        #    self.space_code_provision(self.conf.new_space_code)

        #self.reboot()
        print('\n\n------------------------------------------------------\n\
WARNING: now you should change network paramaters and guarantee the device\n\
         can connect to Internet. Further more, you should change pointcode\n\
         and device id manually. DO Not forget to reboot the device to make\n\
         sure it works.')

if __name__ == '__main__':
    d = DeviceUpgrade()
    d.run()

#import os
#import http.client
#import subprocess
#
#def update(bin):
#    if not os.path.exists(bin):
#        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/release/build_park_960p/" + bin + " ."
#        command = "cp /home/durd/work/build/" + bin + " ."
#        print(command)
#        os.system(command)
#    copy2device(bin, "/tmp")
#    run_cmd("/var/ftp/busybox sh /tmp/" + bin)
#    run_cmd("sync")
#
#def httpget(cmd):
#    conn = http.client.HTTPConnection(ip, 80)
#    conn.request("GET", "/index.htm")
#    result = conn.getresponse()
#    print(result.status, result.reason)
#
#    data = result.read()
#    print(data)
#    conn.close()
#
#def httpcfg(cmd):
#    conn = http.client.HTTPConnection(ip, 80)
#    conn.request("GET", "/vb.htm?" + cmd)
#    result = conn.getresponse()
#    print(result.status, result.reason)
#
#    data = result.read()
#    print(data)
#    conn.close()
#
#def run_cmd(cmd):
#    #command = "ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no bit1@" + ip + " \"" + cmd + "\""
#    command = "ssh bit1@" + ip + " \"" + cmd + "\""
#    #print(command)
#    os.system(command)
#
#def run_cmd_concurrent(cmd):
#    command = "ssh tzhtc@" + ip + " \"" + cmd + "\""
#    subprocess.call(cmd, shell=True)
#
#def copy2device(from_path, to_path):
#    command = "scp " + from_path + " bit1@" + ip + ":" + to_path
#    print(command)
#    os.system(command)
#
#def copyfromdevice(from_path, to_path):
#    command = "scp " + "bit1@" + ip + ":" + from_path + " " + to_path
#    print(command)
#    os.system(command)
#
#for item in range(211, 237):
##for item in [211, 216]:
#    #ip = "192.168.8.8"
#    ip = "192.168.1." + str(item)
#    print("\033[95m============ " + ip + " ============\033[0m")
#    try:
#        #httpcfg("timefrequency=-1&datestampenable3=2&sntpip=202.112.7.13")
#        #httpcfg("pt_set_save=4,1,0,58.58.40.162,10000,20000,58.58.40.162,18901,3702")
#        #httpcfg("network_card_type=4")
#        #run_cmd(r"sed -i '1i\ETHTOOL_OPTS=\"speed 10 duplex half autoneg off\"' /mnt/nand/info.cfg")
#        #run_cmd("cat /mnt/nand/platform_set.cfg")
#        #copy2device("/home/durd/work/ipnc_rdk/ipnc_app/vd/build/vd", "/tmp/vd")
#        #run_cmd("mv /tmp/vd /opt/ipnc/vd")
#        #copy2device("/home/durd/work/ipnc_rdk/target/filesys/opt/ipnc/firmware/ipnc_rdk_fw_m3vpss.xem3", "/tmp/ipnc_rdk_fw_m3vpss.xem3")
#        #copy2device("/home/durd/repo/bulk/preview.htm", "/var/www/preview.htm")
#        #run_cmd("mv /tmp/ipnc_rdk_fw_m3vpss.xem3 /opt/ipnc/firmware/ipnc_rdk_fw_m3vpss.xem3")
#        #copy2device("platform_set.cfg", "/mnt/nand")
#        #copy2device("/home/durd/test/package/lrzsz-0.12.20/src/rz", "/usr/bin")
#        #copy2device("/home/durd/test/package/lrzsz-0.12.20/src/sz", "/usr/bin")
#        #run_cmd("cat /var/version/version")
#        #run_cmd("rm -rf /home/records/*")
#        #run_cmd("sync && /sbin/reboot -f &")
#        #os.system("ping " + ip)
#        #run_cmd("/opt/ipnc/pid_status  -q|awk \'NR>4&&(\$6>120||\$8>100) {print  \$4 \\\"\\t\\\" \$6 \\\"\\t\\\" \$8 \\\"\\t\\\" \$9 }\' ")
#        #run_cmd("/opt/ipnc/pid_status  -q|awk \'{print  \$4 \\\"\\t\\\" \$6 \\\"\\t\\\" \$8 \\\"\\t\\\" \$9 }\' ")
#        #run_cmd("uptime")
#        #run_cmd("cat /var/version/version")
#        #run_cmd("killall -9 vd")
#        #run_cmd("tail -f /tmp/log/vd.log")
#        #copy2device("platform_set.cfg", "/mnt/nand/platform_set.cfg")
#        #update("PARK_A04_01_20160413192728_A1.bin")
#        #run_cmd("rm -rf /home/records/*")
#        #run_cmd("killall -9 vd &")
#        run_cmd("cat /var/version/version")
#        run_cmd("ps | grep vd")
#    except Exception as e:
#        print("\033[91m" + ip + " !!!FAILED!!!" + "\033[0m", "\033[93m", e, "\033[0m")
#        continue
#
#"""
#Pre defined actions
#1.  set ntp server
#    httpcfg("timefrequency=-1&datestampenable3=2&sntpip=58.58.40.162")
#2.  set platform for zehin
#    httpcfg("pt_set_save=4,1,0,58.58.40.162,10000,20000,58.58.40.162,18901,3702")
#"""
