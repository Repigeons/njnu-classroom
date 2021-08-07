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


async def handle(jasdm: str) -> list:
    async with aioredis.start(app['redis']) as redis:
        if not await redis.hexists("overview", jasdm):
            raise RequestParameterError('jasdm')

        return json.loads(await redis.hget(
            name="overview",
            key=jasdm
        ))
