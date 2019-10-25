#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import datetime
import json
import traceback

import demjson
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest

from cli.aliyun_base import AliyunBase, readj2


class AliyunSlb(AliyunBase):

    def __init__(self, clent,):
        super(AliyunSlb, self).__init__()
        self.clent = clent
        # self.outjson = outPath
        self.request = DescribeLoadBalancersRequest()
        self.product = 'slb'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            SlbList = response.get('LoadBalancers').get('LoadBalancer')
            slb_list = []
            for item in SlbList:
                slb_list.append({"id": item['LoadBalancerId'], "name": item['LoadBalancerName']})
            return slb_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))
            print('%s %s %s' % (datetime.datetime.now(), str(e), traceback.format_exc()))

    def _card_template(self, index, template, slb_id, slb_name, metric, project, thresholds):
        return demjson.decode(
            template.render(id=(index + 2), h=8, w=4, x=(index % 6) * 4, y=(index % 8) * 8, LoadBalancerId=slb_id,
                            metric=metric,
                            project=project, name=slb_name, thresholds=thresholds))

    def GenerateSlbDashboard(self, slb_list, card_template, panels_template, metric, thresholds, title):
        template = readj2(card_template)
        panels_cards = []
        for i, slb in enumerate(slb_list):
            panels_cards.append(self._card_template(index=i, template=template, slb_id=slb["id"], slb_name=slb["name"],
                                                    metric=metric, project="acs_slb_dashboard",
                                                    thresholds=thresholds))
        template = readj2(panels_template)
        resultjson = template.render(panels_card=demjson.encode(panels_cards), title=title, tag="SLB")
        # print(resultjson)
        # writej2('{0}/{1}.json'.format(self.check_dir(), metric), resultjson)
        # writej2("slb/" + metric + ".json", resultjson)
        return {'cms-{0}.json'.format(metric): resultjson}

    def action(self, ):
        print('Generating SLB config')
        metric_list = [
            {"field": "HeathyServerCount", "name": "后端健康ECS实例个数"},
            {"field": "UnhealthyServerCount", "name": "后端异常ECS实例个数"},
            {"field": "InstanceActiveConnection", "name": "实例每秒活跃连接数"},
            {"field": "InstanceDropConnection", "name": "实例每秒丢失连接数"},
            {"field": "InstanceDropPacketRX", "name": "实例每秒丢失入包数"},
            {"field": "InstanceDropPacketTX", "name": "实例每秒丢失出包数"},
            {"field": "InstanceDropTrafficRX", "name": "实例每秒丢失入bit数"},
            {"field": "InstanceDropTrafficTX", "name": "实例每秒丢失出bit数"},
            {"field": "InstanceInactiveConnection", "name": "实例每秒非活跃连接数"},
            {"field": "InstanceMaxConnection", "name": "实例每秒最大并发连接数"},
            {"field": "InstanceNewConnection", "name": "实例每秒新建连接数"},
            {"field": "InstancePacketRX", "name": "实例每秒入包数"},
            {"field": "InstancePacketTX", "name": "实例每秒出包数"},
            {"field": "InstanceTrafficRX", "name": "实例每秒入bit数"},
            {"field": "InstanceTrafficTX", "name": "实例每秒出bit数"},
            {"field": "InstanceMaxConnectionUtilization", "name": "最大连接数使用率"},
            {"field": "InstanceNewConnectionUtilization", "name": "新建连接数使用率"},
            {"field": "InstanceQps", "name": "实例维度的QPS"},
            {"field": "InstanceRt", "name": "实例维度的请求平均延时"},
            {"field": "InstanceStatusCode2xx", "name": "实例维度的slb返回给client的2xx状态码统计"},
            {"field": "InstanceStatusCode3xx", "name": "实例维度的slb返回给client的3xx状态码统计"},
            {"field": "InstanceStatusCode4xx", "name": "实例维度的slb返回给client4xx状态码统计"},
            {"field": "InstanceStatusCode5xx", "name": "实例维度的slb返回给client的5xx状态码统计"},
            {"field": "InstanceStatusCodeOther", "name": "实例维度的slb返回给client的Other状态码统计"},
            {"field": "InstanceUpstreamCode4xx", "name": "实例维度的rs返回给slb的4xx状态码统计"},
            {"field": "InstanceUpstreamCode5xx", "name": "实例维度的rs返回给slb的5xx状态码统计"},
            {"field": "InstanceUpstreamRt", "name": "实例维度的rs发给proxy的平均请求延迟"},
            {"field": "InstanceQpsUtilization", "name": "QPS使用率"},
        ]
        result_dict = {}
        slb_list = self.load_all()
        for metric in metric_list:
            result_dict.update(
                self.GenerateSlbDashboard(slb_list, "card.json.j2", "dashboard.json.j2", metric.get("field"), "",
                                          metric.get("name")))
        print("Build Success!")
        return result_dict


if __name__ == '__main__':
    slb = AliyunSlb()
    slb.action()
