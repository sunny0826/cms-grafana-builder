#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
from sys import version_info

from setuptools import setup, find_packages

if version_info[:2] < (3, 5):
    raise RuntimeError(
        'Unsupported python version %s.' % '.'.join(version_info)
    )

_NAME = 'cms'
setup(
    name=_NAME,
    version='0.0.2',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    author='Guoxudong',
    author_email='sunnydog0826@gmail.com',
    include_package_data=True,
    install_requires=[
        'aliyun-python-sdk-core==2.13.10',
        'aliyun-python-sdk-core-v3==2.13.10',
        'aliyun-python-sdk-ecs==4.17.5',
        'aliyun-python-sdk-r-kvstore==2.1.2',
        'aliyun-python-sdk-rds==2.3.9',
        'aliyun-python-sdk-slb==3.2.15',
        'aliyun-python-sdk-vpc==3.0.7',
        'aliyun-python-sdk-dds==2.0.7',
        'aliyun-python-sdk-cms==6.0.13',
        'demjson==2.2.4',
        'jmespath==0.9.4',
        'bottle==0.12.18',
        'uwsgi',
    ],
    entry_points={
        'console_scripts': [
            '{0} = cli.runner:main'.format(_NAME),
        ]
    }
)
