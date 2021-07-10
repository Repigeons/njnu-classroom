#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio

from aiohttp import web

from app import app
from . import service
from .controller import *

config = app['config']['application']['server']


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize())
    _main()


async def initialize():
    from app import mail, mysql, redis
    await asyncio.gather(
        mail.initialize(),
        mysql.initialize(),
        redis.initialize(),
    )
    await service.reset()


def _main():
    app.add_routes(routes)
    for middleware in middlewares:
        app.middlewares.append(middleware)
    web.run_app(
        app=app,
        host=config['host'],
        port=config['port'],
    )
