#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
from argparse import ArgumentParser
from os import getenv

from aliyunsdkcore.client import AcsClient

from cli.aliyun_ecs import AliyunEcs
from cli.aliyun_eip import AliyunEip
from cli.aliyun_rds import AliyunRds
from cli.aliyun_redis import AliyunRedis
from cli.aliyun_slb import AliyunSlb
from cli.k8s import handle_k8s


def load_arg(accessKeyId, accessSecret, regionId):
    return AcsClient(accessKeyId, accessSecret, regionId)


def handle(specs, outPath):
    print('Start generating json configuration!')
    print('Generating ECS config')
    rds = AliyunEcs(specs, outPath)
    rds.action()
    print('Generating RDS config')
    rds = AliyunRds(specs, outPath)
    rds.action()
    print('Generating EIP config')
    eip = AliyunEip(specs, outPath)
    eip.action()
    print('Generating Redis config')
    rds = AliyunRedis(specs, outPath)
    rds.action()
    print('Generating SLB config')
    slb = AliyunSlb(specs, outPath)
    slb.action()


def main():
    """
    CMS Grafana builder
    """
    parser = ArgumentParser(
        description='CMS Grafana builder.',
        prog='cmsbuilder'
    )
    parser.add_argument(
        '--access-key-id',
        type=str,
        default=getenv('ACCESS_KEY_ID', ''),
        help='Aliyun accessKeyId'
    )
    parser.add_argument(
        '--access-secret',
        type=str,
        default=getenv('ACCESS_SECRET', ''),
        help='Aliyun accessSecret'
    )
    parser.add_argument(
        '--region-id',
        type=str,
        default=getenv('REGION_ID', 'cn-shanghai'),
        help='aliyun regionId,default:cn-shanghai'
    )
    # parser.add_argument(
    #     '--out-path',
    #     type=str,
    #     default=getenv('OUT_PATH', 'jsonconfig'),
    #     help='result output path'
    # )
    args = parser.parse_args()
    try:
        specs = load_arg(args.access_key_id, args.access_secret, args.region_id)
        handle_k8s(specs)
        # handle(specs, args.out_path)
        print('Success generating json configuration!')
    except KeyboardInterrupt:
        pass

    except Exception as err:
        raise RuntimeError('Oh no! I am dying...') from err


if __name__ == '__main__':
    main()
