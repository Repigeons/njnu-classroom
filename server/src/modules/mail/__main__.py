#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/9/20
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import json
import os
import socket
from email.mime.text import MIMEText

from app import app
from app.mail import smtp_socket_address
from ztxlib import aiosmtp

smtp: aiosmtp.SMTP
config = app['config']['application']['mail']
mail_params = dict(
    header_from="Repigeons",
    header_to="南师教室运维人员",
    receivers=[receiver['addr'] for receiver in config['receivers']],
)


def main():
    initialize()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(startup())


def initialize():
    # Initialize smtp
    global smtp
    smtp = aiosmtp.SMTP(
        host=config['sender']['host'],
        port=config['sender']['port'],
        user=config['sender']['user'],
        password=config['sender']['password'],
    )
    # Initialize unix domain socket
    if os.path.exists(smtp_socket_address):
        os.unlink(smtp_socket_address)


async def startup():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(smtp_socket_address)
    while True:
        try:
            data = json.loads(sock.recv(1024))
            subject, content = data['subject'], data['content']
        except (json.decoder.JSONDecodeError, KeyError, TypeError):
            continue
        async with smtp:
            await smtp.send(
                **mail_params,
                subject=subject,
                mime_parts=[MIMEText(content)]
            )
