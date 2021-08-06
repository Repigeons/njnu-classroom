#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import logging

import aiofiles
import yaml
from aiohttp.web import Application

app = Application()


async def initialize():
    config = "resources/application.yml"
    try:
        async with aiofiles.open(config, 'rb') as f:
            app['config'] = yaml.safe_load(await f.read())
    except FileNotFoundError:
        logging.critical("FileNotFoundError: No such file [%s]", config)
        logging.info("Exit with code %d", -1)
        exit(-1)


async def finalize():
    try:
        app['redis'].close()
    except KeyError:
        pass
