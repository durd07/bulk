#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import subprocess

def run_cmd(ip, cmd):
    command = "ssh -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no bit1@" + ip + " \"" + cmd + "\""
    #command = "ssh bit1@" + ip + " \"" + cmd + "\""
    #print(command)
    #os.system(command)
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print e

def copy2device(ip, from_path, to_path):
    command = "scp -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no " + from_path + " bit1@" + ip + ":" + to_path
    print(command)
    os.system(command)

def update(ip, bin):
    if not os.path.exists(bin):
        #command = "scp " + "durd@192.168.1.164:/home/durd/dm8127/svn_jenkins/release/build_park_960p/" + bin + " ."
        command = "cp /home/durd/dm8127/jenkins/park/release/bin/" + bin + " ."
        print(command)
        os.system(command)
    copy2device(ip, bin, "/tmp")
    run_cmd(ip, "/var/ftp/busybox sh /tmp/" + bin)
    run_cmd(ip, "sync")
    run_cmd(ip, "/sbin/reboot -f &")
