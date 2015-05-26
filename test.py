#!/usr/bin/python_old
#coding=utf-8
import json, Queue
import urllib2
import socket
import struct
import simplejson
import yaml,time,urllib2
from multiprocessing.pool import ThreadPool as Pool
q = Queue.Queue()
url = "http://192.168.7.77:8082/api_jsonrpc.php"
header = {"Content-Type":"application/json"}
def auth_key():     
    data = json.dumps(
    {
       "jsonrpc": "2.0",
       "method": "user.login",
       "params": {
       "user": "chenzhongyi",
       "password": "9595062690"
    },
    "id": 0
    })
    request = urllib2.Request(url,data)
    for key in header:
       request.add_header(key,header[key])
    try:
       result = urllib2.urlopen(request)
    except URLError as e:
       print "Auth Failed, Please Check Your Name AndPassword:",e.code
    else:
       response = json.loads(result.read())
       result.close()
    return response['result']
def metric():
    data = json.dumps(
    {
       "jsonrpc":"2.0",
       "method":"host.get",
       "params":{
           "output":["hostid","name"],
           "groupids":"48",
       },
       "auth":auth_key(), 
       "id":1,
    })
    request = urllib2.Request(url,data)
    for key in header:
       request.add_header(key,header[key])
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
       for host in response['result']:
           data = json.dumps(
           {
              "jsonrpc":"2.0",
              "method":"item.get",
              "params":{
                  "output":["itemids","key_"],
                  "hostids":host['hostid'],
              },
              "auth": auth_key() , 
              "id":1,
           })
           request = urllib2.Request(url,data)
           for key in header:
              request.add_header(key,header[key])
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
              for hosts in response['result']:
		  q.put(host['name']+"."+hosts['key_'])


metric()


class ZabbixSender:
    zbx_header = 'ZBXD'
    zbx_version = 1
    zbx_sender_data = {u'request': u'sender data', u'data': []}
    send_data = ''
    def __init__(self, server_host, server_port = 10051):
        self.server_ip = socket.gethostbyname(server_host)
        self.server_port = server_port
    def AddData(self, host, key, value, clock = None):
        add_data = {u'host': host, u'key': key, u'value': value}
        if clock != None:
            add_data[u'clock'] = clock
        self.zbx_sender_data['data'].append(add_data)
        return self.zbx_sender_data
    def ClearData(self):
        self.zbx_sender_data['data'] = []
        return self.zbx_sender_data
    def __MakeSendData(self):
        zbx_sender_json = simplejson.dumps(self.zbx_sender_data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        json_byte = len(zbx_sender_json)
        self.send_data = struct.pack("<4sBq" + str(json_byte) + "s", self.zbx_header, self.zbx_version, json_byte, zbx_sender_json)
    def Send(self):
        self.__MakeSendData()
        so = socket.socket()
        so.connect((self.server_ip, self.server_port))
        wobj = so.makefile(u'wb')
        wobj.write(self.send_data)
        wobj.close()
        robj = so.makefile(u'rb')
        recv_data = robj.read()
        robj.close()
        so.close()
        tmp_data = struct.unpack("<4sBq" + str(len(recv_data) - struct.calcsize("<4sBq")) + "s", recv_data)
        recv_json = simplejson.loads(tmp_data[3])
	glosend_data = ''
        return recv_data
if __name__ == '__main__':
    while 1:
            sender = ZabbixSender(u'192.168.7.77')
            metric_value=q.get(block=True)
	    host,key=metric_value.split('.')
            url="http://127.0.0.1/render/?target=%s&from=-10second&format=json"%metric_value
            try:
                res = urllib2.urlopen(url)
                data = yaml.load(res)
            except:
                pass
            if len(data) and 'datapoints' in data[0]:
                data = filter(lambda d: d[0] != None, data[0]['datapoints'])
            for graphite_values in data: sender.AddData(u'%s'%host, u'%s'%key, u'%s'%graphite_values[0])
            res = sender.Send()
	    print "#####################################"
            print sender.send_data
	    print "#####################################"
            print res
