#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from ztxlib import aioredis
from .app import app

__all__ = (
    'initialize',
)


async def initialize():
    config = app['config']['database']['redis']
    app['redis'] = await aioredis.create_pool(
        address=(
            config['host'],
            config['port'],
        ),
        db=config['db'],
    )
