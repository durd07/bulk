#!/usr/bin/env python3

import csv
import http.client
import logging
import logging.handlers
import time

#spaceCode,spaceNo,spaceContent,spaceUsed,spaceType,isBook,devCode,lastSpaceCode,issave,parkCode




def httppost(ip, cmd, body, headers):
    global logger
    conn = http.client.HTTPConnection(ip, 80, timeout=4)
    conn.request("POST", cmd, body, headers)
    result = conn.getresponse()
    print(result.status, result.reason)
    logger.info(result.status.__str__() + " " + result.reason.__str__())

    data = result.read()
    print(data.decode('utf-8'))
    logger.info(data)
    conn.close()
    #return data

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
    headers = {}
    headers['Accept'] = '*/*'
    headers['Origin'] = 'http://www.teyiting.com'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Referer'] = 'http://www.teyiting.com/commonCache.jsp'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'
    # The cookie should be changed each time.
    headers['Cookie'] = 'SESSION_COOKIE=14; JSESSIONID=88F953268D8A212BCCE29CE426E1613F; autoLogin=no'

    body = ''
    #with open('data.csv', newline='') as csvfile:
    #    data_list = csv.reader(csvfile, delimiter=',', quotechar='|')
    #    for row in data_list:
    #        if row[0].startswith('#'):
    #            continue
    #        [spaceCode,spaceNo,spaceContent,spaceUsed,spaceType,isBook,devCode,lastSpaceCode,issave,parkCode] = row

    #        body = 'spaceCode=' + spaceCode + '&' \
    #             + 'spaceNo=' + spaceNo   + '&' \
    #             + 'spaceContent=' + spaceContent + '&' \
    #             + 'spaceUsed=' + spaceUsed + '&' \
    #             + 'spaceType=' + spaceType + '&' \
    #             + 'isBook=' + isBook + '&' \
    #             + 'devCode=' + devCode + '&' \
    #             + 'lastSpaceCode=' + lastSpaceCode + '&' \
    #             + 'issave=' + issave + '&' \
    #             + 'parkCode=' + parkCode + '\n\n'
    #        print(body)
    #        #print(headers)
    space_code = 370212001007
    while True:
        url = 'teyiting.com'
        cmd = '/commonQuery/catchPic.do?spaceCode=' + str(space_code)
        space_code += 1
        if space_code == 370212001027:
            space_code = 370212001007
        httppost(url, cmd, body, headers)
        #time.sleep(0.1)

if __name__ == '__main__':
    main()
