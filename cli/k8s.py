#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import json
import os
from os import getenv

from kubernetes import client, config


def handle_k8s():
    config.load_incluster_config()
    k8s_apps_v1 = client.CoreV1Api()
    namespace = getenv('INIT_POD_NAMESPACE', 'default')
    dep = client.V1ConfigMap(
        data=generate_config_map()
    )
    resp = k8s_apps_v1.patch_namespaced_config_map(name='grafana-cms-dashboards', namespace=namespace, body=dep)
    print("ConfigMap update. name='%s'" % resp.metadata.name)


def generate_config_map():
    config_map_dict = {}
    for root, dirs, files in os.walk("../model"):
        for file in files:
            # with open("/var/local/model/{0}".format(filename), "r") as fd:
            with open(os.path.join(root, file), "r") as fd:
                config_map_dict.update({file: json.loads(fd.read())})

    return config_map_dict
