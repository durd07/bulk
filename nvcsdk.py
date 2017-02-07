#!/usr/bin/env python
# -*- codeing: utf-8 -*-

'''
send udp request one by one, then get the response about
device info,
the result is saved in result.xml, you can drag it into
excel for format.
'''

import csv
from xmlutils.xml2csv import xml2csv
import logging
import socket
import time
from xml.dom.minidom import parse, parseString
from xml.dom.minidom import Document

doc = Document()
root = doc.createElement('Probe')
doc.appendChild(root)

class Tag():
    def __init__(self):
        pass

def sendRequest(ip):
    address = (ip, 7000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(5)

    msg = r'''<?xml version="1.0" encoding="UTF-8"?>
            <Probe>
              <Types>NetworkVideoTransmitter</Types>
              <Serial/>
              <IPv4/>
              <MacAddr/>
              <GateWay/>
              <NetMask/>
              <Firmware/>
              <Hardware/>
              <Temperature/>
              <UpTime/>
              <RebootCount/>
              <WisReboot/>
              <BoaReboot/>
              <ProcessAbort/>
              <MsgInQueue/>
              <MemLeak/>
              <CpuUtilization/>
              <MemUtilization/>
              <FlashUtilization/>
              </Probe>'''
    s.sendto(msg, address)
    #time.sleep(0.2)
    data, addr = s.recvfrom(2048)
    #print 'received: ', data.strip('\x00'), 'from', addr
    parseXml(data)

def parseXml(string):
    global root
    doc = parseString(string.strip('\x00').replace('\n', ''))
    for node in doc.getElementsByTagName('GetDeviceInformationResponse'):
       root.appendChild(node)
#        ID = node.getAttribute('ID')
#        num = node.getElementsByTagName('num')[0].firstChild.nodeValue
#        name = node.getElementsByTagName('name')[0].firstChild.nodeValue
#        tag = Tag()
#        tag.ID = ID
#        tag.num = num
#        tag.name = name
#        tagList1.append(tag)

def do_action(space_code, ip):
    try:
        print('%s %s' % (space_code, ip))
        #logger.info(ip + " " + space_code)
        #print("\033[95m============ " + ip + " ===== " + space_code + "=======\033[0m")
        sendRequest(ip)
        return True
    except Exception as e:
        #logger.error('%s %s' % (ip, e))
        print('%s %s' % (ip, e))
        #print("\033[91m" + ip + " !!!FAILED!!!" + "\033[0m", "\033[93m", e, "\033[0m")
        return False

def main():
    with open('ip.csv') as csvfile:
        ip_list = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in ip_list:
            if row[0].startswith('#'):
                continue
            [space_code, ip] = row
            if not do_action(space_code, ip):
                continue
    global doc
    f = open('result.xml', 'w')
    string = doc.toprettyxml(indent = '  ').replace('        \n', '')
    f.write(string)
    f.close

    #print
    import xml.etree.cElementTree as ET
    root = ET.fromstring(string)

#    print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
#    'Serial', 'IPv4', 'NetMask', 'GateWay', 'MacAddr', 'Hardware', 'Firmware', 'UpTime', 'CpuUtilization', 'MemUtilization', 'FlashUtilization', 'RebootCount', 'BoaReboot', 'WisReboot', 'MemLeak', 'MsgInQueue', 'ProcessAbort', 'Temperature')
#    for item in root.findall('GetDeviceInformationResponse'):
#        Serial           = item.find('Serial').text
#        IPv4             = item.find('IPv4').text
#        NetMask          = item.find('NetMask').text
#        GateWay          = item.find('GateWay').text
#        MacAddr          = item.find('MacAddr').text
#        Hardware         = item.find('Hardware').text
#        Firmware         = item.find('Firmware').text
#        UpTime           = item.find('UpTime').text
#        CpuUtilization   = item.find('CpuUtilization').text
#        MemUtilization   = item.find('MemUtilization').text
#        FlashUtilization = item.find('FlashUtilization').text
#        RebootCount      = item.find('RebootCount').text
#        BoaReboot        = item.find('BoaReboot').text
#        WisReboot        = item.find('WisReboot').text
#        MemLeak          = item.find('MemLeak').text
#        MsgInQueue       = item.find('MsgInQueue').text
#        ProcessAbort     = item.find('ProcessAbort').text
#        Temperature      = item.find('Temperature').text
#        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (
#        Serial, IPv4, NetMask, GateWay, MacAddr, Hardware, Firmware, UpTime, CpuUtilization, MemUtilization, FlashUtilization, RebootCount, BoaReboot, WisReboot, MemLeak, MsgInQueue, ProcessAbort, Temperature)

if __name__ == '__main__':
    main()
#tagList1 = []
#tagList2 = []
#
#with open('space.csv') as csvfile:
#    ip_list = csv.reader(csvfile, delimiter=',', quotechar='|')
#    for row in ip_list:
#        if row[0].startswith('#'):
#            continue
#        [name, num] = row
#        tag = Tag()
#        tag.ID = 0
#        tag.num = num
#        tag.name = name
#        tagList2.append(tag)
#
#doc = parse('tag_config.xml')
#for node in doc.getElementsByTagName('Berth'):
#    ID = node.getAttribute('ID')
#    num = node.getElementsByTagName('num')[0].firstChild.nodeValue
#    name = node.getElementsByTagName('name')[0].firstChild.nodeValue
#    tag = Tag()
#    tag.ID = ID
#    tag.num = num
#    tag.name = name
#    tagList1.append(tag)
#
##doc = parse('tag_config2.xml')
##for node in doc.getElementsByTagName('Berth'):
##    ID = node.getAttribute('ID')
##    num = node.getElementsByTagName('num')[0].firstChild.nodeValue
##    name = node.getElementsByTagName('name')[0].firstChild.nodeValue
##    tag = Tag()
##    tag.ID = ID
##    tag.num = num
##    tag.name = name
##    tagList2.append(tag)
#
#for tag2 in tagList2:
#    hasKey = False
#    for tag1 in tagList1:
#        if tag1.name == tag2.name:
#            tag1.num = tag2.num
#            hasKey = True
#
#    if hasKey == False:
#        tagList1.append(tag2)
#
## sort
#tagList1 = sorted(tagList1, key=lambda tag: tag.name)
#
## find the dup item
#exists_name = set()
#exists_num = set()
#for item in tagList1:
#    if item.name in exists_name:
#        print "dup name " + item.name
#    if item.num in exists_num:
#        if item.num != "0":
#            print "dup num " + item.num
#    else:
#        exists_num.add(item.num)
#        exists_name.add(item.name)
#
#
#from xml.dom.minidom import Document
#
#doc = Document()
#
#root = doc.createElement('Probe')
#doc.appendChild(root)
#
#i = 1
#for tag in tagList1:
#    item = doc.createElement('Berth')
#    item.setAttribute('ID', str(i))
#    i = i + 1
#    root.appendChild(item)
#    numtag = doc.createElement('num')
#    numtext = doc.createTextNode(tag.num)
#    numtag.appendChild(numtext)
#
#    nametag = doc.createElement('name')
#    nametext = doc.createTextNode(tag.name)
#    nametag.appendChild(nametext)
#    item.appendChild(numtag)
#    item.appendChild(nametag)
#
#f = open('tag_config_new.xml', 'w')
#f.write(doc.toprettyxml(indent = '  '))
#f.close
