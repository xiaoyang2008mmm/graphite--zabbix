#!/usr/bin/python_old
#coding=utf-8
import json
import urllib2
# based url and required header
url = "http://192.168.1.1:8082/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
# auth user and password
data = json.dumps(
{
   "jsonrpc": "2.0",
   "method": "user.login",
   "params": {
   "user": "ch",
   "password": "9"
},
"id": 0
})
# create request object
request = urllib2.Request(url,data)
for key in header:
   request.add_header(key,header[key])
# auth and get authid
try:
   result = urllib2.urlopen(request)
except URLError as e:
   print "Auth Failed, Please Check Your Name AndPassword:",e.code
else:
   response = json.loads(result.read())
   result.close()
print"Auth Successful. The Auth ID Is:",response['result']




data = json.dumps(
{
   "jsonrpc":"2.0",
   "method":"host.get",
   "params":{
       "output":["hostid","name"],
       "groupids":"34",
   },
   "auth":response['result'], # theauth id is what auth script returns, remeber it is string
   "id":1,
})
# create request object
request = urllib2.Request(url,data)
for key in header:
   request.add_header(key,header[key])
# get host list
try:
   result = urllib2.urlopen(request)
except URLError as e:
   if hasattr(e, 'reason'):
       print 'We failed to reach a server.'
       print 'Reason: ', e.reason
   elif hasattr(e, 'code'):
       print 'The server could not fulfill the request.'
       print 'Error code: ', e.code
else:
   response = json.loads(result.read())
   result.close()
   print "Number Of Hosts: ", len(response['result'])
   for host in response['result']:
       print "Host ID:",host['hostid'],"HostName:",host['name']

