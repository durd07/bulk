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
