#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import os

import demjson
from jinja2 import Template


class AliyunBase(object):
    def __init__(self, ):
        self.clent = None
        self.request = None
        self.product = None
        self.outjson = None

    def set_params(self, page=1, page_size=50):
        '''设置请求参数'''
        self.request.set_PageSize(page_size)
        self.request.set_accept_format('json')
        self.request.set_PageNumber(page)

    def line_template(self, template, line_name, line_id, metric, project, ycol, period=300):
        return demjson.decode(
            template.render(name=str(line_name), id=line_id, metric=metric, project=project, period=period, ycol=ycol))

    def panels_template(self, index, template, title, targets, format, redline=80):
        return demjson.decode(
            template.render(id=(index + 3), h=8, w=12, x=(index % 2) * 12, y=(index % 8) * 8, title=str(title),
                            format=format, targets=targets, redline=redline))

    def check_dir(self):
        name = '{0}/{1}'.format(self.outjson, self.product)
        if not os.path.exists(name):
            os.makedirs(name)
        return name

    def action(self, ):
        '''action函数为接口，每个子类都要重写这个方法'''
        raise NotImplemented('you must overwrite this method!')


def readj2(filename):
    with open("/var/local/model/{0}".format(filename), "r") as fd:
        template = Template(fd.read())
    return template


def writej2(filename, content):
    with open(filename, "w") as f:
        f.write(content)
