#!/usr/bin.python_old
# -*- coding: utf-8 -*-
import socket
import struct
import simplejson
import yaml,time,urllib2
from multiprocessing.pool import ThreadPool as Pool
def getGraphiteData():
        url="http://127.0.0.1/render/?target=system.loadavg_1min&from=-10second&format=json"

        s_time = time.time()
        try:
            res = urllib2.urlopen(url)
            data = yaml.load(res)
        except:
            pass
        finally:
            e_time = time.time() - s_time
            e_time = int(e_time)
           # print "{time}ms      {url}".format(time = e_time, url = url)
        if len(data) and 'datapoints' in data[0]:
            data = filter(lambda d: d[0] != None, data[0]['datapoints'])
        return data
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
                return recv_data
if __name__ == '__main__':
        sender = ZabbixSender(u'192.168.7.77')
	for graphite_values in getGraphiteData(): sender.AddData(u'logstash', u'graphite', u'%s'%graphite_values[0])
        res = sender.Send()
        print sender.send_data
        print res

