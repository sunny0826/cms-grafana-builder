#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import datetime
import json
import traceback

import demjson
from aliyunsdkr_kvstore.request.v20150101.DescribeInstancesRequest import DescribeInstancesRequest

from cli.aliyun_base import AliyunBase, readj2, writej2


class AliyunRedis(AliyunBase):

    def __init__(self, clent, outPath):
        super(AliyunRedis, self).__init__()
        self.clent = clent
        self.outjson = outPath
        self.request = DescribeInstancesRequest()
        self.product = 'redis'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            RedisList = response.get('Instances').get('KVStoreInstance')
            redis_list = []
            for item in RedisList:
                redis_list.append({"id": item['InstanceId'], "name": item['InstanceName']})
            return redis_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))
            print('%s %s %s' % (datetime.datetime.now(), str(e), traceback.format_exc()))

    def GenerateRedisDashboard(self, redis_list, line_template, panels_template, metric_list):
        dashboard_lines = []
        for index, metric in enumerate(metric_list):
            panels_lines = []
            for i, redis in enumerate(redis_list):
                template = readj2(line_template)
                panels_lines.append(
                    self.line_template(template=template, line_name=redis['name'], line_id=redis['id'], ycol="Average",
                                       metric=metric['field'], project="acs_kvstore"))
            template = readj2(panels_template)
            dashboard_lines.append(
                self.panels_template(index=index, template=template, title=metric['name'], format=metric['format'],
                                     redline=metric['redline'], targets=demjson.encode(panels_lines)))
        dashboard_template = readj2("dashboard.json.j2")
        resultjson = dashboard_template.render(panels_card=demjson.encode(dashboard_lines), title="redis资源监控",
                                               tag="Redis")
        print(resultjson)
        writej2('{0}/{1}.json'.format(self.check_dir(), self.product), resultjson)
        # writej2("redis/redis.json", resultjson)

    def action(self, ):
        metric_list = [
            # {"field": "Standardappend", "name": "append 命令的执行频率", "format": "cps"},
            # {"field": "Standardbitcount", "name": "bitcount 命令的执行频率", "format": "cps"},
            # {"field": "Standardbitop", "name": "bitop 命令的执行频率", "format": "cps"},
            # {"field": "Standardblpop", "name": "blpop 命令的执行频率", "format": "cps"},
            # {"field": "Standardbrpop", "name": "brpop 命令的执行频率", "format": "cps"},
            # {"field": "Standardbrpoplpush", "name": "brpoplpush 命令的执行频率", "format": "cps"},
            # {"field": "Standarddecr", "name": "decr 命令的执行频率", "format": "cps"},
            # {"field": "Standarddecrby", "name": "decrby 命令的执行频率", "format": "cps"},
            # {"field": "Standarddel", "name": "del 命令的执行频率", "format": "cps"},
            # {"field": "Standarddiscard", "name": "discard 命令的执行频率", "format": "cps"},
            # {"field": "Standarddump", "name": "dump 命令的执行频率", "format": "cps"},
            # {"field": "Standardexec", "name": "exec 命令的执行频率", "format": "cps"},
            # {"field": "Standardexists", "name": "exists 命令的执行频率", "format": "cps"},
            # {"field": "Standardexpire", "name": "expire 命令的执行频率", "format": "cps"},
            # {"field": "Standardexpireat", "name": "expireat 命令的执行频率", "format": "cps"},
            # {"field": "StandardExpires", "name": "Expires 命令的执行次数", "format": "cps"},
            # {"field": "StandardFailedCount", "name": "命令失败次数", "format": "cps"},
            # {"field": "Standardget", "name": "get 命令的执行频率", "format": "cps"},
            # {"field": "CpuUsage", "name": "CPU使用率", "format": "percent"},
            # {"field": "MemoryUsage", "name": "内存使用率", "format": "percent"},
            # {"field": "FailedCount", "name": "操作失败数", "format": "percent"},
            # {"field": "IntranetIn", "name": "内网网络入流量", "format": "bps"},
            # {"field": "IntranetInRatio", "name": "写入带宽使用率", "format": "percent"},
            # {"field": "IntranetOut", "name": "内网网络出流量", "format": "bps"},
            # {"field": "IntranetOutRatio", "name": "读取带宽使用率", "format": "percent"},
            # {"field": "TPS", "name": "同步速度", "format": "percent"},
            # {"field": "UsedConnection", "name": "已用连接数", "format": "percent"},
            # {"field": "UsedMemory", "name": "内存使用量", "format": "percent"},
            # {"field": "UsedQPS", "name": "已用QPS数量", "format": "percent"},
            {"field": "StandardCpuUsage", "name": "CPU 使用率", "format": "percent", "redline": "80"},
            {"field": "StandardMemoryUsage", "name": "内存使用率", "format": "percent", "redline": "80"},
            {"field": "StandardQPSUsage", "name": "QPS使用率", "format": "percent", "redline": "80"},
            {"field": "StandardConnectionUsage", "name": "连接数使用率", "format": "percent", "redline": "80"},
            {"field": "StandardUsedConnection", "name": "已用连接数", "format": "short", "redline": "1000"},
            {"field": "StandardUsedQPS", "name": "平均每秒访问次数", "format": "short", "redline": "1000"},
            {"field": "StandardAvgRt", "name": "平均响应时间", "format": "µs", "redline": "1000"},
            {"field": "StandardMaxRt", "name": "最大响应时间", "format": "µs", "redline": "5000"},
            {"field": "StandardIntranetIn", "name": "流入带宽", "format": "bps", "redline": "1000"},
            {"field": "StandardIntranetInRatio", "name": "流入带宽使用率", "format": "percent", "redline": "80"},
            {"field": "StandardIntranetOut", "name": "流出带宽", "format": "bps", "redline": "80"},
            {"field": "StandardKeys", "name": "缓存内 Key 数量", "format": "short", "redline": "80000"},
        ]
        redis_list = self.load_all()
        self.GenerateRedisDashboard(redis_list, "line.json.j2", "linePanels.json.j2", metric_list)
        print("build success!")


if __name__ == '__main__':
    rds = AliyunRedis()
    rds.action()
