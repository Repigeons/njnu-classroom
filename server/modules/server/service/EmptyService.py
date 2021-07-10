#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json

from app import app
from ztxlib import aioredis


async def handle(args: dict) -> list:
    async with aioredis.start(app['redis']) as redis:
        if 'day' not in args.keys() or not args['day'].isdigit() or not (0 <= int(args['day']) <= 6):
            raise KeyError('day')
        elif 'dqjc' not in args.keys() or not args['dqjc'].isdigit():
            raise KeyError('dqjc')
        elif 'jxl' not in args.keys() or not await redis.hexists("empty", f"{args['jxl']}_{args['day']}"):
            raise KeyError('jxl')

        jxl, day, dqjc = args['jxl'], int(args['day']), int(args['dqjc'])

        value = json.loads(await redis.hget(
            name="empty",
            key=f"{args['jxl']}_{args['day']}"
        ))

    classrooms = []
    for classroom in value:
        if classroom['jc_ks'] <= dqjc <= classroom['jc_js']:
            classrooms.append(classroom)
    for i in range(len(classrooms)):
        classrooms[i]['id'] = i + 1

    return classrooms
