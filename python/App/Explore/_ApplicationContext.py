#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/2/19
# @Author   :  ZhouTianxing
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
shuttle: dict

__send_email: Any


def send_email(subject: str, message: str):
    __send_email(subject=subject, message=message)


def __init__():
    start_time = time.time() * 1000
    logging.info("Initializing ApplicationContext...")

    yml = yaml.safe_load(open(os.getenv("application.yml")))
    __init__base_field(config=yml['application']['explore'])
    __init__mail_server(config=yml['mail'])
    __init__shuttle(config=yml['application']['explore']['shuttle'])

    complete_time = time.time() * 1000
    logging.info("ApplicationContext: initialization completed in %d ms", complete_time - start_time)


def __init__base_field(config: dict) -> None:
    global host, port
    host = config['host']
    port = config['port']


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
    global shuttle
    with open(config['resource'], encoding='utf8') as f:
        stream = f.read().split('\n\n')
        f.close()
    stations = [
        {'name': sp[0], 'position': [float(sp[1]), float(sp[2])]}
        for sp in [station.split('|') for station in stream[0].split(',')]
    ]
    direction1 = [
        line.split(',')
        for line in stream[1].split()
    ]
    direction2 = [
        line.split(',')
        for line in stream[2].split()
    ]
    shuttle = {
        'stations': stations,
        'direction1': direction1,
        'direction2': direction2,
    }


__init__()
