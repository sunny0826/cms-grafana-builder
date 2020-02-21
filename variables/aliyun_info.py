#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import json
import math

from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest
from aliyunsdkslb.request.v20140515.DescribeLoadBalancersRequest import DescribeLoadBalancersRequest
from aliyunsdkvpc.request.v20160428.DescribeEipAddressesRequest import DescribeEipAddressesRequest
from aliyunsdkr_kvstore.request.v20150101.DescribeInstancesRequest import DescribeInstancesRequest as RedisInstances
from aliyunsdkdds.request.v20151201.DescribeDBInstancesRequest import DescribeDBInstancesRequest as MongoDBInstances


class AliyunBase(object):
    def __init__(self, ):
        self.clent = None
        self.request = None
        self.product = None
        self.page = 1
        self.page_size = 50

    def set_params(self, ):
        '''设置请求参数'''
        self.request.set_PageSize(self.page_size)
        self.request.set_accept_format('json')
        self.request.set_PageNumber(self.page)

    def action(self, ):
        '''action函数为接口，每个子类都要重写这个方法'''
        raise NotImplemented('you must overwrite this method!')


class AliyunEcs(AliyunBase):

    def __init__(self, clent):
        super(AliyunEcs, self).__init__()
        self.clent = clent
        self.request = DescribeInstancesRequest()
        self.product = 'ecs'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            total_count = response.get('TotalCount')
            EcsList = response.get('Instances').get('Instance')
            if total_count > self.page_size:
                all_num = math.ceil(total_count / self.page_size)
                for i in range(2, all_num + 1):
                    self.page = i
                    self.set_params()
                    response = json.loads(self.clent.do_action_with_exception(self.request))
                    EcsList.extend(response.get('Instances').get('Instance'))
            ecs_list = []
            for item in EcsList:
                ecs_list.append((item['InstanceId'], item['InstanceName'],
                                 item['NetworkInterfaces']['NetworkInterface'][0]['PrimaryIpAddress']))
            return ecs_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))


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
            total_count = response.get('TotalRecordCount')
            if total_count > self.page_size:
                all_num = math.ceil(total_count / self.page_size)
                for i in range(2, all_num + 1):
                    self.page = i
                    self.set_params()
                    response = json.loads(self.clent.do_action_with_exception(self.request))
                    RdsList.extend(response.get('Items').get('DBInstance'))
            rds_list = []
            for item in RdsList:
                rds_list.append((item['DBInstanceId'], item['DBInstanceDescription']))
            return rds_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))


class AliyunSlb(AliyunBase):

    def __init__(self, clent, ):
        super(AliyunSlb, self).__init__()
        self.clent = clent
        self.request = DescribeLoadBalancersRequest()
        self.product = 'slb'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            SlbList = response.get('LoadBalancers').get('LoadBalancer')
            total_count = response.get('TotalCount')
            if total_count > self.page_size:
                all_num = math.ceil(total_count / self.page_size)
                for i in range(2, all_num + 1):
                    self.page = i
                    self.set_params()
                    response = json.loads(self.clent.do_action_with_exception(self.request))
                    SlbList.extend(response.get('LoadBalancers').get('LoadBalancer'))
            slb_list = []
            for item in SlbList:
                slb_list.append((item['LoadBalancerId'], item['LoadBalancerName']))
            return slb_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))


class AliyunEip(AliyunBase):

    def __init__(self, clent):
        super(AliyunEip, self).__init__()
        self.clent = clent
        self.request = DescribeEipAddressesRequest()
        self.product = 'eip'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            EipList = response.get('EipAddresses').get('EipAddress')
            total_count = response.get('TotalCount')
            if total_count > self.page_size:
                all_num = math.ceil(total_count / self.page_size)
                for i in range(2, all_num + 1):
                    self.page = i
                    self.set_params()
                    response = json.loads(self.clent.do_action_with_exception(self.request))
                    EipList.extend(response.get('EipAddresses').get('EipAddress'))
            epi_list = []
            for item in EipList:
                epi_list.append((item['AllocationId'], item['Name'] + ":" + item['IpAddress']))
            return epi_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))


class AliyunRedis(AliyunBase):

    def __init__(self, clent):
        super(AliyunRedis, self).__init__()
        self.clent = clent
        self.request = RedisInstances()
        self.product = 'redis'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            RedisList = response.get('Instances').get('KVStoreInstance')
            total_count = response.get('TotalCount')
            if total_count > self.page_size:
                all_num = math.ceil(total_count / self.page_size)
                for i in range(2, all_num + 1):
                    self.page = i
                    self.set_params()
                    response = json.loads(self.clent.do_action_with_exception(self.request))
                    RedisList.extend(response.get('Instances').get('KVStoreInstance'))
            redis_list = []
            for item in RedisList:
                redis_list.append((item['InstanceId'], item['InstanceName']))
            return redis_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))

class AliyunMongoDB(AliyunBase):

    def __init__(self, clent):
        super(AliyunMongoDB, self).__init__()
        self.clent = clent
        self.request = MongoDBInstances()
        self.product = 'mongodb'

    def load_all(self, ):
        try:
            self.set_params()
            response = json.loads(self.clent.do_action_with_exception(self.request))
            MongoList = response.get('DBInstances').get('DBInstance')
            total_count = response.get('TotalCount')
            if total_count > self.page_size:
                all_num = math.ceil(total_count / self.page_size)
                for i in range(2, all_num + 1):
                    self.page = i
                    self.set_params()
                    response = json.loads(self.clent.do_action_with_exception(self.request))
                    MongoList.extend(response.get('DBInstances').get('DBInstance'))
            mongo_list = []
            for item in MongoList:
                mongo_list.append((item['DBInstanceId'], item['DBInstanceDescription']))
            return mongo_list
        except Exception as e:
            print('请求阿里云失败，%s', str(e))
