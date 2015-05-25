#!/usr/bin/env python_old
#coding:utf-8
import sys
import time
import urllib2
import yaml

from multiprocessing.pool import ThreadPool as Pool

try:
    from zabbix.api import ZabbixAPI
    from zabbix.sender import ZabbixSender, ZabbixMetric
except:
    print("Zabbix 模块没有安装")
    exit()


#class G2ZProxyException(Exception):
#    pass

class CHEN(object):
    def __init__(self, pattern='graphite*',
                zabbix_url='http://localhost',
                zabbix_user='admin',
                zabbix_pass='zabbix',
                graphite_url='http://localhost',
                threads='1'):

        self.cn = self.__class__.__name__

        self.pattern = pattern
        self.zabbix_url = zabbix_url
        self.graphite_url = 'http://192.168.7.173/render?from=-5minutes&rawData=true&target={req}&format=json'
        self.zapi = ZabbixAPI(self.zabbix_url, user=zabbix_user, password=zabbix_pass)
        self.threads = threads
        self._main()

    def _getHostsFromMetrics(self, metrics):

        hostids = list(set(map(lambda x: int(x['hostid']), metrics)))

        hostids = self.zapi.host.get(hostids = hostids, output = ['name'])

        hosts = {}
        for m in hostids:
            hosts.update({ int(m['hostid']): m['name'] })


        return hosts

    def _getMonitoredMetrics(self):

        result = None
        if self.zapi:
            metrics = self.zapi.item.get(
                search = { 'key_': self.pattern },
                searchWildcardsEnabled = True,
                monitored = True,
                output = ['key_', 'hostid'])
            result = metrics

        return result


    def _getMetrics(self):

        result = None
        metrics = self._getMonitoredMetrics()
        hosts = self._getHostsFromMetrics(metrics)

        self.key = metrics[0]['key_'][0:metrics[0]['key_'].find('[')]
        key_len = len(self.key)

        def metrics_filter(m):
            return {
                'host': hosts[int(m['hostid'])],
                'metric': m['key_'][key_len + 1:-1],
            }

        result = map(metrics_filter, metrics)

        return result

    def _createGraphiteRequest(self, metric):

        result = None

        params = map(lambda x: x.strip(), metric['metric'].split(';'))

        if len(params) > 1:
            req_metric = '{0}.{1}'.format(metric['host'], params[0])
            req = params[1].format(metric=req_metric)
        else:
            req = '{host}.{metric}'

        req = req.format(host = metric['host'], metric = metric['metric'])

        result = self.graphite_url.format(req = req)

        return result

    def _getGraphiteData(self):

        def getData(metric):
            url = self._createGraphiteRequest(metric)

            s_time = time.time()
            try:
                res = urllib2.urlopen(url)
                data = yaml.load(res)
            except:
                pass 
            finally:
                e_time = time.time() - s_time
                e_time = int(e_time * 1000)
                print "{time}ms/t{url}".format(time = e_time, url = url)

            if len(data) and 'datapoints' in data[0]:
                data = filter(lambda d: d[0] != None, data[0]['datapoints'])

                if data:
                    len_data = len(data)
                    data = [ v / len_data for v in reduce(lambda x, y: [ x[0] + y[0], x[1] + y[1] ], data) ]
                    metric.update({ 'value': data[0], 'time': data[1] })

        pool = Pool(processes=50)
        pool.map(getData, self.metrics)
        pool.close()
        pool.join()

    def _main(self):

        self.metrics = self._getMetrics()

        self._getGraphiteData()

        msg = []
        for m in self.metrics:
            if 'value' in m:
                metric = '{0}[{1}]'.format(self.key, m['metric'])
                msg.append(ZabbixMetric(m['host'], metric, m['value'], m['time']))

        ZabbixSender(use_config=True).send(msg)
        print(len(self.metrics))

if __name__ == '__main__':

    CHEN(zabbix_url = "http://192.168.7.7:8082",
            zabbix_user = "ch",
            zabbix_pass = "959",
            graphite_url = "http://192.168.7.9",
            threads = 50)
