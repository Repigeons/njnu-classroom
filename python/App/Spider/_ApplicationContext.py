#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/1/10 0010
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
from redis import ConnectionPool

from utils import MariaDB, SMTP

account: dict
selenium: dict

mysql: MariaDB
redis_pool: ConnectionPool

__send_email: Any


def send_email(subject: str, message: str):
    __send_email(subject=subject, message=message)


def __init__():
    start_time = time.time() * 1000
    logging.info("Initializing ApplicationContext...")

    yml = yaml.safe_load(open(os.getenv('application.yml')))
    __init__base_field(config=yml['application']['spider'])
    __init__mysql(config=yml['database']['mysql'])
    __init__redis(config=yml['database']['redis'])
    __init__mail_server(config=yml['mail'])

    complete_time = time.time() * 1000
    logging.info("ApplicationContext: initialization completed in %d ms", complete_time - start_time)


def __init__base_field(config: dict) -> None:
    global account, selenium
    selenium = config['selenium']
    account = config['account']


def __init__mysql(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing MariaDBConnectionPool...")

    global mysql
    mysql = MariaDB(name="Spider", **config)

    complete_time = time.time() * 1000
    logging.info("MariaDBConnectionPool: initialization completed in %d ms", complete_time - start_time)


def __init__redis(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing RedisConnectionPool...")

    global redis_pool
    redis_pool = ConnectionPool(**config)

    complete_time = time.time() * 1000
    logging.info("RedisConnectionPool: initialization completed in %d ms", complete_time - start_time)


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
