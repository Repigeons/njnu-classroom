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
from collections import namedtuple
from email.mime.text import MIMEText
from threading import Thread

import yaml

from utils import SMTP

host: str
port: int
token: str
file: str

__mail: namedtuple('MailConfig', ['function', 'receivers'])


def send_email(subject: str, message: str):
    Thread(
        target=__mail.function,
        kwargs={
            'subject': subject,
            'header_from': "Repigeons",
            'header_to': "南师教室运维人员",
            'receivers': [receiver['addr'] for receiver in __mail.receivers],
            'mime_parts': [MIMEText(message)]
        }
    ).start()


def __init__():
    start_time = time.time() * 1000
    logging.info("Initializing ApplicationContext...")

    yml = yaml.safe_load(open(os.path.join(os.getenv("resources"), "application.yml")))
    __init__base_field(config=yml['application']['notice'])
    __init__mail(config=yml['mail'])

    complete_time = time.time() * 1000
    logging.info("ApplicationContext: initialization completed in %d ms", complete_time - start_time)


def __init__base_field(config: dict) -> None:
    global host, port
    global token, file
    host, port = config['host'], config['port']
    token, file = config['token'], config['file']


def __init__mail(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing SMTPServer...")

    global __mail
    __mail = namedtuple('MailConfig', ['function', 'receivers'])(
        function=SMTP(**config['sender']).send,
        receivers=config['receivers']
    )

    complete_time = time.time() * 1000
    logging.info("SMTPServer: initialization completed in %d ms", complete_time - start_time)


__init__()
