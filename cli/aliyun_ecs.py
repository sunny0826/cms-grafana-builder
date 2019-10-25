#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import datetime
import json
import traceback

import demjson
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest

from cli.aliyun_base import AliyunBase, readj2


class AliyunEcs(AliyunBase):

    def __init__(self, clent):
        super(AliyunEcs, self).__init__()
        self.clent = clent
        # self.outjson = outPath
        self.request = DescribeInstancesRequest()
        self.product = 'ecs'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            EcsList = response.get('Instances').get('Instance')
            ecs_list = []
            for item in EcsList:
                ecs_list.append({"id": item['InstanceId'], "name": item['InstanceName']})
            return ecs_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))
            print('%s %s %s' % (datetime.datetime.now(), str(e), traceback.format_exc()))

    def panels_template(self, index, template, title, targets, format, redline=80):
        return demjson.decode(
            template.render(id=(index + 3), h=8, w=24, x=0, y=(index % 8) * 8, title=str(title),
                            format=format, targets=targets, redline=redline))

    def GenerateEcsDashboard(self, ecs_list, line_template, panels_template, metric_list):
        dashboard_lines = []
        for index, metric in enumerate(metric_list):
            panels_lines = []
            for i, ecs in enumerate(ecs_list):
                template = readj2(line_template)
                panels_lines.append(
                    self.line_template(template=template, line_name=ecs['name'], line_id=ecs['id'], ycol="Average",
                                       period=60, metric=metric['field'], project="acs_ecs_dashboard"))
            template = readj2(panels_template)
            dashboard_lines.append(
                self.panels_template(index=index, template=template, title=metric['name'], format=metric['format'],
                                     redline=metric['redline'], targets=demjson.encode(panels_lines)))
        dashboard_template = readj2("dashboard.json.j2")
        resultjson = dashboard_template.render(panels_card=demjson.encode(dashboard_lines), title="ECS资源监控",
                                               tag="ECS")
        # print(resultjson)
        # writej2('{0}/{1}.json'.format(self.check_dir(), self.product), resultjson)
        # writej2("ecs/ecs.json", resultjson)
        return {'cms-{0}.json'.format(self.product): resultjson}

    def action(self, ):
        print('Generating ECS config')
        metric_list = [
            {"field": "cpu_total", "name": "CPU 使用率", "format": "percent", "redline": "80"},
            {"field": "memory_usedutilization", "name": "内存使用率", "format": "percent", "redline": "80"},
            {"field": "diskusage_utilization", "name": "磁盘使用率", "format": "percent", "redline": "80"},
            {"field": "IntranetInRate", "name": "私网流入带宽", "format": "bps", "redline": "1000"},
            {"field": "IntranetOutRate", "name": "私网流出带宽", "format": "bps", "redline": "1000"},
            {"field": "DiskReadIOPS", "name": "系统磁盘读IOPS", "format": "cps", "redline": "1000"},
            {"field": "DiskWriteIOPS", "name": "系统磁盘写IOPS", "format": "cps", "redline": "1000"},
        ]
        ecs_list = self.load_all()
        print("build success!")
        return self.GenerateEcsDashboard(ecs_list, "line.json.j2", "linePanels.json.j2", metric_list)


if __name__ == '__main__':
    rds = AliyunEcs()
    rds.action()
