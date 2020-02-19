#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import base64
from argparse import ArgumentParser
from os import getenv

from aliyunsdkcore.client import AcsClient

from cli.k8s import handle_k8s


def load_arg(accessKeyId, accessSecret, regionId):
    return AcsClient(accessKeyId, accessSecret, regionId)


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
    args = parser.parse_args()
    try:
        access_key_id = base64.b64encode(args.access_key_id.encode("utf-8"))
        access_secret = base64.b64encode(args.access_secret.encode("utf-8"))
        specs = load_arg(str(access_key_id), str(access_secret), args.region_id)
        handle_k8s(specs)
        print('Success generating json configuration!')
    except KeyboardInterrupt:
        pass

    except Exception as err:
        raise RuntimeError('Oh no! I am dying...') from err


if __name__ == '__main__':
    main()
