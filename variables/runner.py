#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import re
import sqlite3
from argparse import ArgumentParser
from os import getenv

from aliyunsdkcore.client import AcsClient
from bottle import (Bottle, HTTPResponse, request, response, json_dumps as dumps, run)

from variables.aliyun_info import AliyunSlb, AliyunRds, AliyunEip, AliyunRedis, AliyunMongoDB
from variables.db import initDB, refresh_other, refresh_ecs

app = Bottle()


@app.hook('after_request')
def enable_cors():
    print("after_request hook")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route("/", method=['GET', 'OPTIONS'])
def index():
    return "UP"


@app.post('/search')
def search():
    conn = sqlite3.connect('/app/db/cms.db')
    cursor = conn.cursor()
    print(request.json)
    produce_type = request.json['target']
    if produce_type.startswith('ecs_ip('):
        cursor.execute('select ip from ecs where name=?',
                       (re.findall(r'[(](.*?)[)]', produce_type.replace('\\', ''))), )
        values = cursor.fetchall()
        body = values[0]
    elif '(' in produce_type:
        sql = 'select id from {0} where name="{1}"'.format(
            produce_type.split('(')[0], re.findall(r'[(](.*?)[)]', produce_type.replace('\\', ''))[0])
        print(sql)
        cursor.execute(sql)
        values = cursor.fetchall()
        body = values[0]
    else:
        cursor.execute('select name from {0}'.format(produce_type))
        values = cursor.fetchall()
        body = []
        for value in values:
            body.append(value[0])
    cursor.close()
    conn.close()
    return HTTPResponse(body=dumps(body), headers={'Content-Type': 'application/json'})


def load_arg(accessKeyId, accessSecret, regionId):
    return AcsClient(accessKeyId, accessSecret, regionId)


def refresh(args):
    initDB()
    specs = load_arg(args.access_key_id, args.access_secret, args.region_id)
    refresh_ecs(specs)
    rds = AliyunRds(specs)
    refresh_other('rds', rds)
    slb = AliyunSlb(specs)
    refresh_other('slb', slb)
    eip = AliyunEip(specs)
    refresh_other('eip', eip)
    redis = AliyunRedis(specs)
    refresh_other('redis', redis)
    mongodb = AliyunMongoDB(specs)
    refresh_other('mongodb', mongodb)


def get_parser():
    parser = ArgumentParser(
        description='CMS Grafana variables runner.',
        prog='runner'
    )
    subparsers = parser.add_subparsers(help='sub-command help')
    run_parser = subparsers.add_parser('run', help='run backend')
    run_parser.add_argument(
        '--port',
        type=int,
        default=getenv('RUN_PORT', 8088),
        help='Runner Port'
    )

    run_parser.set_defaults(func=runner)
    refresh_parser = subparsers.add_parser('refresh', help='refresh resource')
    refresh_parser.set_defaults(func=refresh)
    refresh_parser.add_argument(
        '--access-key-id',
        type=str,
        default=getenv('ACCESS_KEY_ID', ''),
        help='Aliyun accessKeyId'
    )
    refresh_parser.add_argument(
        '--access-secret',
        type=str,
        default=getenv('ACCESS_SECRET', ''),
        help='Aliyun accessSecret'
    )
    refresh_parser.add_argument(
        '--region-id',
        type=str,
        default=getenv('REGION_ID', 'cn-shanghai'),
        help='aliyun regionId,default:cn-shanghai'
    )

    return parser

def runner(args):
    run(app=app, host='0.0.0.0', port=args.port)


def main():
    parser = get_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        pass

    except Exception as err:
        raise RuntimeError('Oh no! I am dying...') from err


if __name__ == '__main__':
    main()
