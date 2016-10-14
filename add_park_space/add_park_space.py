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
    headers['Origin'] = 'http://htc.taizhou.gov.cn'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    headers['Referer'] = 'http://htc.taizhou.gov.cn/systemManager/parkManage.do?k=1'
    headers['Accept-Encoding'] = 'gzip, deflate'
    headers['Accept-Language'] = 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2'
    # The cookie should be changed each time.
    headers['Cookie'] = 'SESSION_COOKIE=14; JSESSIONID=45E70DD9CB666F73E75FB31E000957D0; autoLogin=no'

    with open('data.csv', newline='') as csvfile:
        data_list = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in data_list:
            if row[0].startswith('#'):
                continue
            [spaceCode,spaceNo,spaceContent,spaceUsed,spaceType,isBook,devCode,lastSpaceCode,issave,parkCode] = row

            body = 'spaceCode=' + spaceCode + '&' \
                 + 'spaceNo=' + spaceNo   + '&' \
                 + 'spaceContent=' + spaceContent + '&' \
                 + 'spaceUsed=' + spaceUsed + '&' \
                 + 'spaceType=' + spaceType + '&' \
                 + 'isBook=' + isBook + '&' \
                 + 'devCode=' + devCode + '&' \
                 + 'lastSpaceCode=' + lastSpaceCode + '&' \
                 + 'issave=' + issave + '&' \
                 + 'parkCode=' + parkCode + '    \n'
            print(body)
            #print(headers)
            url = 'htc.taizhou.gov.cn'
            cmd = '/infoSpace/updateInfoSpaceObj.do'
            httppost(url, cmd, body, headers)
            time.sleep(2)

if __name__ == '__main__':
    main()
