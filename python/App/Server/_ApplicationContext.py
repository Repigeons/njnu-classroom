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
from redis import ConnectionPool

from utils import MariaDB, SMTP

host: str
port: int
serve: bool
day_mapper: dict

mysql: MariaDB
redis_pool: ConnectionPool

__send_email: Any


def send_email(subject: str, message: str):
    __send_email(subject=subject, message=message)


def __init__():
    start_time = time.time() * 1000
    logging.info("Initializing ApplicationContext...")

    yml = yaml.safe_load(open(os.path.join(os.getenv("resources"), "application.yml")))
    __init__base_field(config=yml['application']['server'])
    __init__mysql(config=yml['database']['mysql'])
    __init__redis(config=yml['database']['redis'])
    __init__mail_server(config=yml['mail'])

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

    global mysql_reset, mysql_search, mysql_feedback
    mysql_reset = MariaDB(name="Server_reset", **config)
    mysql_search = MariaDB(name="Server_search", **config)
    mysql_feedback = MariaDB(name="Server_feedback", **config)

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
