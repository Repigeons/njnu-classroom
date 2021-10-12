#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
import logging
import socket

from .app import app

smtp_socket_address = './run/mail.sock'

__all__ = (
    'initialize',
    'smtp_socket_address',
)


async def initialize():
    try:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        sock.connect(smtp_socket_address)

        app['mail'] = lambda **kwargs: sock.send(
            json.dumps(kwargs).encode(encoding='utf8')
        )
    except AttributeError as e:
        # Windows调试不发送邮件
        app['mail'] = lambda **kwargs: logging.error(json.dumps(kwargs, ensure_ascii=False))
