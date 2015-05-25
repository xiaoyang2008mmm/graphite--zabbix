#!/usr/bin/python_lod
import yaml,time,urllib2
from multiprocessing.pool import ThreadPool as Pool
def getGraphiteData():
	url="http://127.0.0.1/render/?target=system.loadavg_1min&from=-10second&format=json"

        s_time = time.time()
        try:
            res = urllib2.urlopen(url)
            data = yaml.load(res)
        except:
            print "没有数据返回"
        if len(data) and 'datapoints' in data[0]:
            data = filter(lambda d: d[0] != None, data[0]['datapoints'])
	    len_data = len(data)
	    for graphite_values in data: print graphite_values[0]

getGraphiteData()
