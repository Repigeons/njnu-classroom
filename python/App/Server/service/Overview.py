#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Overview.py
""""""
import json

from redis import StrictRedis
from redis_lock import Lock

from utils.aop import autowired, configuration


@autowired()
def redis_pool(): pass


@configuration("application.server.service")
def serve(): pass


def handle_overview(args: dict) -> dict:
    if not serve:
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    redis = StrictRedis(connection_pool=redis_pool)
    lock = Lock(redis, "Server-Overview")
    if lock.acquire():
        try:
            if 'jasdm' not in args.keys() or not redis.hexists("Overview", args['jasdm']):
                raise KeyError('jasdm')

            value = json.loads(redis.hget(
                name="Overview",
                key=args['jasdm']
            ))

            return {
                'status': 0,
                'message': "ok",
                'service': "on",
                'data': value
            }
        finally:
            lock.release()
