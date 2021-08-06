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
        if 'jasdm' not in args.keys() or not await redis.hexists("overview", args['jasdm']):
            raise KeyError('jasdm')

        return json.loads(await redis.hget(
            name="overview",
            key=args['jasdm']
        ))
