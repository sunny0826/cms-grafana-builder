#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
from os import getenv

from kubernetes import client, config

from cli.aliyun_ecs import AliyunEcs
from cli.aliyun_eip import AliyunEip
from cli.aliyun_rds import AliyunRds
from cli.aliyun_redis import AliyunRedis


# from cli.aliyun_slb import AliyunSlb


def handle_k8s(specs):
    config.load_incluster_config()
    k8s_apps_v1 = client.CoreV1Api()
    namespace = getenv('INIT_POD_NAMESPACE', 'default')
    dep = client.V1ConfigMap(
        data=config_map_data(specs)
    )
    resp = k8s_apps_v1.patch_namespaced_config_map(name='grafana-cms-dashboards', namespace=namespace, body=dep)

    print("ConfigMap update. name='%s'" % resp.metadata.name)


def config_map_data(specs):
    config_map_dict = {}
    print('Start generating json configuration!')

    rds = AliyunEcs(specs)
    config_map_dict.update(rds.action())

    rds = AliyunRds(specs)
    config_map_dict.update(rds.action())

    eip = AliyunEip(specs)
    config_map_dict.update(eip.action())

    rds = AliyunRedis(specs)
    config_map_dict.update(rds.action())

    # slb = AliyunSlb(specs)
    # config_map_dict.update(slb.action())
    return config_map_dict
