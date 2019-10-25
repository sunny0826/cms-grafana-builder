#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import datetime
import json
import traceback

import demjson
from aliyunsdkvpc.request.v20160428.DescribeEipAddressesRequest import DescribeEipAddressesRequest

from cli.aliyun_base import AliyunBase, readj2, writej2


class AliyunEip(AliyunBase):

    def __init__(self, clent):
        super(AliyunEip, self).__init__()
        self.clent = clent
        # self.outjson = outPath
        self.request = DescribeEipAddressesRequest()
        self.product = 'eip'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            RedisList = response.get('EipAddresses').get('EipAddress')
            epi_list = []
            for item in RedisList:
                epi_list.append({"id": item['AllocationId'], "name": item['Name'] + ":" + item['IpAddress']})
            return epi_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))
            print('%s %s %s' % (datetime.datetime.now(), str(e), traceback.format_exc()))

    def panels_template(self, index, template, title, targets, format, redline=80):
        return demjson.decode(
            template.render(id=(index + 3), h=8, w=24, x=0, y=(index % 8) * 8, title=str(title),
                            format=format, targets=targets, redline=redline))

    def GenerateEipDashboard(self, epi_list, line_template, panels_template, metric_list):
        dashboard_lines = []
        for index, metric in enumerate(metric_list):
            panels_lines = []
            for i, eip in enumerate(epi_list):
                template = readj2(line_template)
                panels_lines.append(self.line_template(template=template, line_name=eip['name'], line_id=eip['id'],
                                                       ycol=metric['ycol'], metric=metric['field'], period=60,
                                                       project="acs_vpc_eip"))
            template = readj2(panels_template)
            dashboard_lines.append(
                self.panels_template(index=index, template=template, title=metric['name'], format=metric['format'],
                                     redline=metric['redline'], targets=demjson.encode(panels_lines)))
        dashboard_template = readj2("dashboard.json.j2")
        resultjson = dashboard_template.render(panels_card=demjson.encode(dashboard_lines), title="EIP监控",
                                               tag="EIP")
        # print(resultjson)
        # writej2('{0}/{1}.json'.format(self.check_dir(), self.product), resultjson)
        # writej2("eip/eip.json", resultjson)
        return {'cms-{0}.json'.format(self.product): resultjson}

    def action(self, ):
        print('Generating EIP config')
        metric_list = [
            {"field": "net_tx.rate", "name": "流出带宽", "format": "bps", "redline": "8000000", "ycol": "Value"},
            {"field": "net_rx.rate", "name": "流入带宽", "format": "bps", "redline": "8000000", "ycol": "Value"},
            {"field": "net_txPkgs.rate", "name": "每秒流出数据包数", "format": "cps", "redline": "150000", "ycol": "Value"},
            {"field": "net_rxPkgs.rate", "name": "每秒流入数据包数", "format": "cps", "redline": "150000", "ycol": "Value"},
            {"field": "out_ratelimit_drop_speed", "name": "限速丢包速率", "format": "percent", "redline": "5",
             "ycol": "Average"},
        ]
        eip_list = self.load_all()
        print("build success!")
        return self.GenerateEipDashboard(eip_list, "line.json.j2", "linePanels.json.j2", metric_list)


if __name__ == '__main__':
    eip = AliyunEip()
    eip.action()
