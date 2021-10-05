#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
import socket

from .app import app

smtp_socket_address = './run/mail.sock'

__all__ = (
    'initialize',
    'smtp_socket_address',
)


async def initialize():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.connect(smtp_socket_address)

    app['mail'] = lambda **kwargs: sock.send(
        json.dumps(kwargs).encode(encoding='utf8')
    )
