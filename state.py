#!/usr/bin/python3
import os
import time
import json
import http.client
from subprocess import Popen, PIPE

#while True:
#cmd = "curl -l -H \"Content-Type: application/x-www-form-urlencoded; charset=UTF-8\" -X POST -d \'page=1&rows=100\'  http://58.58.40.162:18080/vpaas/getTerminaInfoList.action\?domainId\=9acc6d8ecc59496eb5b98a4d56fb809d\&state\=100 | python2 -m json.tool | grep -E \"terminalSn|terminalState\""
cmd = "curl -l -H \"Content-Type: application/x-www-form-urlencoded; charset=UTF-8\" -X POST -d \'page=1&rows=100\'  http://58.58.40.162:18080/vpaas/getTerminaInfoList.action\?domainId\=9acc6d8ecc59496eb5b98a4d56fb809d\&state\=100 | python2 -m json.tool"
#os.system(cmd)
p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
out = p.communicate()
print(json.loads(out).tostr())
#    time.sleep(5)
