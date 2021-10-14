#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json

from app import app
from exceptions import RequestParameterError
from ztxlib import aioredis


async def handle(jxl: str, day: str, dqjc: int) -> list:
    async with aioredis.start(app['redis']) as redis:
        if day not in ['Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.']:
            raise RequestParameterError('day')
        if not (1 <= dqjc <= 12):
            raise RequestParameterError('dqjc')
        if not await redis.hexists("empty", f"{jxl}:{day}"):
            raise RequestParameterError('jxl')
        value = json.loads(await redis.hget("empty", f"{jxl}:{day}"))

    classrooms = []
    for classroom in value:
        if classroom['jc_ks'] <= dqjc <= classroom['jc_js']:
            classrooms.append(classroom)
    for i in range(len(classrooms)):
        classrooms[i]['id'] = i + 1

    return classrooms
