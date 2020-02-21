#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import sqlite3

from variables.aliyun_info import AliyunEcs, AliyunRds, AliyunSlb


def initDB():
    print("init DB")
    try:
        conn = sqlite3.connect('/app/db/cms.db')
        cursor = conn.cursor()
        cursor.execute('create table if not EXISTS ecs (id varchar(20) primary key, name varchar(20), ip varchar(20))')
        cursor.execute('create table if not EXISTS rds (id varchar(20) primary key, name varchar(20))')
        cursor.execute('create table if not EXISTS slb (id varchar(20) primary key, name varchar(20))')
        cursor.execute('create table if not EXISTS eip (id varchar(20) primary key, name varchar(20))')
        cursor.execute('create table if not EXISTS redis (id varchar(20) primary key, name varchar(20))')
        cursor.execute('create table if not EXISTS mongodb (id varchar(20) primary key, name varchar(20))')
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print('初始化数据库失败，%s', str(e))


def refresh_ecs(specs):
    try:
        conn = sqlite3.connect('/app/db/cms.db')
        cursor = conn.cursor()
        ecs = AliyunEcs(specs)
        ecs_list = ecs.load_all()
        cursor.execute('delete from ecs')
        cursor.execute('insert into ecs (id, name, ip) values {0}'.format(str(ecs_list).strip('[]')))
        print('rowcount =', cursor.rowcount)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print('获取ECS信息失败，%s', str(e))


def refresh_other(product, cls):
    try:
        print('refresh info of {0}'.format(product))
        conn = sqlite3.connect('/app/db/cms.db')
        cursor = conn.cursor()
        client = cls
        plist = client.load_all()
        cursor.execute('delete from {0}'.format(product))
        cursor.execute('insert into {0} (id, name) values {1}'.format(product, str(plist).strip('[]')))
        print('rowcount =', cursor.rowcount)
        cursor.close()
        conn.commit()
        conn.close()
    except Exception as e:
        print('获取{0}信息失败，{1}'.format(product, e))
