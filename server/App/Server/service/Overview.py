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

from ztxlib.rpspring import Autowired
from ztxlib.rpspring import Value


class __Application:
    @Autowired
    def redis_pool(self): pass

    @Value("application.server.service")
    def serve(self) -> bool: pass


def handle_overview(args: dict) -> dict:
    if not __Application.serve:
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    redis = StrictRedis(connection_pool=__Application.redis_pool)
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
