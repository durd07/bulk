#!/usr/bin/python3
import os
import http.client
import socket
import time
import logging
import logging.handlers

MAX_FAILER = 2
INTERVAL_TIME = 300
TIMEOUT = 4

#ip_list = ["192.168.1.193"]
#request_path = "/openEpark/servertest.do"
#java_home = "/usr/java/jdk1.7.0_67"
#bin_path = "/home/durd/apache-tomcat-7.0.70/bin"

ip_list = ["htc.taizhou.gov.cn"]
request_path = "/api/inspectorate/spaceManage.do?watchmanCode=f9554da6825c468caa0826b9215c0e43"
java_home = "/root/jdk1.7"
bin_path = "/root/apache-tomcat-7.0.70/bin"

shutdown_cmd = "export JAVA_HOME=" + java_home + " && " + bin_path + "/shutdown.sh &"
startup_cmd = "export JAVA_HOME=" + java_home + " && " + bin_path + "/startup.sh &"

class server:
    def __init__(self, ip):
        self.ip = ip
        self.rotate_count = 0

def httpget(ip, cmd):
    conn = http.client.HTTPConnection(ip, 80, timeout=TIMEOUT)
    conn.request("GET", cmd)
    result = conn.getresponse()
    logger.info(result.status.__str__() + " " + result.reason.__str__())

    data = result.read()
    #logger.info(data)
    conn.close()
    #return data

def run_cmd(ip, cmd):
    command = "ssh -oConnectTimeout=10 -oBatchMode=yes -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no root@" + ip + " \"" + cmd + "\""
    logger.info(command)
    #command = "ssh root@" + ip + " \"" + cmd + "\""
    #print(command)
    os.system(command)

def log_init():
    global logger
    LOG_FILE = 'test.log'
    handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 100)
    fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logger = logging.getLogger('test')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

def main():
    global logger
    log_init()
    logger.error("@@@server monitor start@@@")
    server_list = []

    #for item in range(193, 194):
    #    ip = "192.168.1." + str(item)
    for ip in ip_list:
        #print("\033[95m============ " + ip + " ============\033[0m\n")
        logger.info("============ " + ip + " ============")
        serv = server(ip)
        server_list.append(serv)

    while True:
        for item in server_list:
            try:
                data = httpget(item.ip, request_path)

                # only on sucess can drop in this case.
                item.rotate_count = 0
            except Exception as e:
                #print(e)
                logger.error(item.ip + " !!!FAILED!!!" + e.__str__())
                #if type(e) is socket.timeout:
                #    item.rotate_count += 1
                #if item.rotate_count >= MAX_FAILER:
                #    item.rotate_count = 0
                #    logger.error(item.ip + " restart the service.")
                #    run_cmd(item.ip, shutdown_cmd)
                #    #run_cmd("192.168.1.153", shutdown_cmd)

                #    time.sleep(5)
                #    run_cmd(item.ip, startup_cmd)
                #    #run_cmd("192.168.1.153", startup_cmd)
                continue
        time.sleep(INTERVAL_TIME)

if __name__ == '__main__':
    main()
