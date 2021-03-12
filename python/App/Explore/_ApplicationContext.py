#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/2/19
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _ApplicationContext.py
""""""
import csv
import logging
import os
import time
from threading import Thread
from typing import Any

import yaml
from redis import ConnectionPool

from utils import SMTP, MariaDB

host: str
port: int
shuttle: dict
stations: list

redis_pool: ConnectionPool
mysql: MariaDB
__send_email: Any


def send_email(subject: str, message: str):
    __send_email(subject=subject, message=message)


def __init__():
    start_time = time.time() * 1000
    logging.info("Initializing ApplicationContext...")

    yml = yaml.safe_load(open(os.path.join(os.getenv("resources"), "application.yml")))
    __init__base_field(config=yml['application']['explore'])
    __init__mail_server(config=yml['mail'])
    __init__shuttle(config=yml['application']['explore']['shuttle'])
    __init__mysql(config=yml['database']['mysql'])
    __init__redis(config=yml['database']['redis'])

    complete_time = time.time() * 1000
    logging.info("ApplicationContext: initialization completed in %d ms", complete_time - start_time)


def __init__base_field(config: dict) -> None:
    global host, port
    host = config['host']
    port = config['port']


def __init__redis(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing RedisConnectionPool...")

    global redis_pool
    redis_pool = ConnectionPool(**config)

    complete_time = time.time() * 1000
    logging.info("RedisConnectionPool: initialization completed in %d ms", complete_time - start_time)


def __init__mysql(config: dict) -> None:
    start_time = time.time() * 1000
    logging.info("Initializing MariaDBConnectionPool...")

    global mysql_reset, mysql_search, mysql_feedback
    mysql_reset = MariaDB(name="Server_reset", **config)
    mysql_search = MariaDB(name="Server_search", **config)
    mysql_feedback = MariaDB(name="Server_feedback", **config)

    complete_time = time.time() * 1000
    logging.info("MariaDBConnectionPool: initialization completed in %d ms", complete_time - start_time)


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


def __init__shuttle(config: dict) -> None:
    global stations
    stations = [
        {
            'name': row['name'],
            'position': [
                float(row['latitude']),
                float(row['longitude'])
            ]
        }
        for row in csv.DictReader(
            open(os.path.join(os.getenv("resources"), config['resource']), encoding='utf8')
        )
    ]


__init__()
