#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import datetime
import json
import traceback

import demjson
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest

from cli.aliyun_base import AliyunBase, readj2


class AliyunRds(AliyunBase):

    def __init__(self, clent):
        super(AliyunRds, self).__init__()
        self.clent = clent
        self.request = DescribeDBInstancesRequest()
        self.product = 'rds'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            RdsList = response.get('Items').get('DBInstance')
            rds_list = []
            for item in RdsList:
                rds_list.append({"id": item['DBInstanceId'], "name": item['DBInstanceDescription']})
            return rds_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))
            print('%s %s %s' % (datetime.datetime.now(), str(e), traceback.format_exc()))

    def GenerateRdsDashboard(self, rds_list, line_template, panels_template, metric_list):
        dashboard_lines = []
        for index, metric in enumerate(metric_list):
            panels_lines = []
            for i, rds in enumerate(rds_list):
                template = readj2(line_template)
                panels_lines.append(
                    self.line_template(template=template, line_name=rds['name'], line_id=rds['id'], ycol="Average",
                                       metric=metric['field'], project="acs_rds_dashboard"))
            template = readj2(panels_template)
            dashboard_lines.append(
                self.panels_template(index=index, template=template, title=metric['name'], format=metric['format'],
                                     targets=demjson.encode(panels_lines)))
        dashboard_template = readj2("dashboard.json.j2")
        resultjson = dashboard_template.render(panels_card=demjson.encode(dashboard_lines), title="RDS监控", tag="RDS")
        # print(resultjson)
        return {'cms-{0}.json'.format(self.product): resultjson}

    def action(self, ):
        print('Generating RDS config')
        # metric_list = [
        #     {"field": "CpuUsage", "name": "CPU使用率", "format": "percent"},
        #     {"field": "DiskUsage", "name": "磁盘使用率", "format": "percent"},
        #     {"field": "IOPSUsage", "name": "IOPS使用率", "format": "percent"},
        #     {"field": "ConnectionUsage", "name": "连接数使用率", "format": "percent"},
        #     {"field": "DataDelay", "name": "只读实例延迟", "format": "s"},
        #     {"field": "MemoryUsage", "name": "内存使用率", "format": "percent"},
        #     {"field": "MySQL_NetworkOutNew", "name": "Mysql每秒网络出流量", "format": "bps"},
        #     {"field": "MySQL_NetworkInNew", "name": "Mysql每秒网络入流量", "format": "bps"},
        #     {"field": "MySQL_ActiveSessions", "name": "Mysql当前活跃Sessions数", "format": "short"},
        # ]
        metric_list = self.read_metric_config_map('rds')
        rds_list = self.load_all()
        print("build success!")
        return self.GenerateRdsDashboard(rds_list, "line.json.j2", "linePanels.json.j2", metric_list)
