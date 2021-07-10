#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from .app import app
from ztxlib import aiosmtp

__all__ = (
    'initialize',
)


async def initialize():
    config = app['config']['mail']
    app['smtp'] = aiosmtp.SMTP(
        host=config['sender']['host'],
        port=config['sender']['port'],
        user=config['sender']['user'],
        password=config['sender']['password'],
    )
    app['mail'] = dict(
        header_from="Repigeons",
        header_to="南师教室运维人员",
        receivers=[receiver['addr'] for receiver in config['receivers']],
    )
