#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from .app import app
from ztxlib import aiomysql

__all__ = (
    'initialize',
)


async def initialize():
    config = app['config']['database']['mysql']
    app['mysql'] = await aiomysql.create_pool(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database'],
    )
