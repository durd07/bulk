#!/usr/bin/env python3


####################################################
# CONFIGURATION
####################################################

class device_configuration():
    def __init__(self):
        self.ip = '192.168.1.211'
        self.user = 'root'
        self.passwd = 'bitcom12346'

        self.change_network = True
        self.new_ip = '192.168.8.8'
        self.new_netmask = '255.255.128.0'
        self.new_gateway = '192.168.1.1'
        self.new_dns1 = '192.168.1.1'
        self.new_dns2 = '114.114.114.114'

        self.firmware_update = True
        self.new_firmware_version = 'PARK_A04_01_20161012A1_full.bin'

        self.update_time_config = True
        self.new_ntp_server = '202.112.7.13'
        self.new_ntp_interval = 3600
        self.new_ntp_type = 2

        self.enable_openvpn = False
        self.client_key_path = ''
        self.client_crt_path = ''

        self.provision_space_code = True
        self.new_space_code = '370212101001'

        self.reback_to_original_network = True
