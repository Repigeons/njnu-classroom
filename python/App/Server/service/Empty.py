#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Empty.py
""""""
import json
from typing import Dict, Any

from redis import StrictRedis
from redis_lock import Lock

from utils.aop import autowired, configuration


@autowired()
def redis_pool(): pass


@configuration("application.server.service")
def serve(): pass


def handle_empty(args: Dict[str, str]) -> Dict[str, Any]:
    if not serve:
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    redis = StrictRedis(connection_pool=redis_pool)
    lock = Lock(redis, "Server-Empty")
    if lock.acquire():
        try:
            if 'day' not in args.keys() or not args['day'].isdigit() or not (0 <= int(args['day']) <= 6):
                raise KeyError('day')
            elif 'dqjc' not in args.keys() or not args['dqjc'].isdigit():
                raise KeyError('dqjc')
            elif 'jxl' not in args.keys() or not redis.hexists("Empty", f"{args['jxl']}_{args['day']}"):
                raise KeyError('jxl')

            jxl, day, dqjc = args['jxl'], int(args['day']), int(args['dqjc'])

            value = json.loads(redis.hget(
                name="Empty",
                key=f"{args['jxl']}_{args['day']}"
            ))

            classrooms = []
            for classroom in value:
                if classroom['jc_ks'] <= dqjc <= classroom['jc_js']:
                    classrooms.append(classroom)
            for i in range(len(classrooms)):
                classrooms[i]['id'] = i + 1

            return {
                'status': 0,
                'message': "ok",
                'service': "on",
                'data': classrooms
            }
        finally:
            lock.release()
