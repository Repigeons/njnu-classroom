#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/1/11 0011
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _ApplicationContext.py
""""""
import logging
import os
import time
from threading import Thread
from typing import Any

import yaml

from utils import SMTP

host: str
port: int
token: str
file: str

__send_email: Any


def send_email(subject: str, message: str):
    __send_email(subject=subject, message=message)


def __init__():
    start_time = time.time() * 1000
    logging.info("Initializing ApplicationContext...")

    yml = yaml.safe_load(open(os.path.join(os.getenv("resources"), "application.yml")))
    __init__base_field(config=yml['application']['notice'])
    __init__mail_server(config=yml['mail'])

    complete_time = time.time() * 1000
    logging.info("ApplicationContext: initialization completed in %d ms", complete_time - start_time)


def __init__base_field(config: dict) -> None:
    global host, port
    global token, file
    host, port = config['host'], config['port']
    token, file = config['token'], config['file']


def __init__mail_server(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing SMTPServer...")

    global __send_email
    mail_server = SMTP(**config['sender'])

    def _send_email(subject: str, message: str):
        Thread(
            target=mail_server.send,
            args=(
                subject, message, "plain",
                "Repigeons<info@njnu.xyz>",
                *config['receivers']
            )
        ).start()

    __send_email = _send_email

    complete_time = time.time() * 1000
    logging.info("SMTPServer: initialization completed in %d ms", complete_time - start_time)


__init__()
