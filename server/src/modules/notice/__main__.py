#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio

from aiohttp import web

from app import app
from .controller import *

config = app['config']['application']['notice']


def main():
    app.add_routes(routes)
    for middleware in middlewares:
        app.middlewares.append(middleware)
    web.run_app(
        app=app,
        host=config['host'],
        port=config['port'],
    )
