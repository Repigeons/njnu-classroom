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
from redis import ConnectionPool

from utils import MariaDB, SMTP

host: str
port: int
serve: bool
day_mapper: dict

mysql: MariaDB
redis_pool: ConnectionPool

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
    __init__base_field(config=yml['application']['server'])
    __init__mysql(config=yml['database']['mysql'])
    __init__redis(config=yml['database']['redis'])
    __init__mail(config=yml['mail'])

    complete_time = time.time() * 1000
    logging.info("ApplicationContext: initialization completed in %d ms", complete_time - start_time)


def __init__base_field(config: dict) -> None:
    global host, port, serve
    global day_mapper
    host = config['host']
    port = config['port']
    serve = config['service']
    day_mapper = {
        0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday',
        'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6,
    }


def __init__mysql(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing MariaDBConnectionPool...")

    global mysql
    mysql = MariaDB(name="Server", **config)

    complete_time = time.time() * 1000
    logging.info("MariaDBConnectionPool: initialization completed in %d ms", complete_time - start_time)


def __init__redis(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing RedisConnectionPool...")

    global redis_pool
    redis_pool = ConnectionPool(**config)

    complete_time = time.time() * 1000
    logging.info("RedisConnectionPool: initialization completed in %d ms", complete_time - start_time)


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
