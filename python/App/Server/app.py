#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  service.py
""""""
import logging
import time
from wsgiref.simple_server import make_server

from flask import Flask

from utils.aop import bean, configuration


@bean()
def day_mapper():
    return {
        0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday',
        'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6,
    }


@configuration("application.server.host")
def host(): pass


@configuration("application.server.port")
def port(): pass


start_time = time.time() * 1000
logging.info("Initializing FlaskApplication...")
app = Flask(__name__)
complete_time = time.time() * 1000
logging.info("FlaskApplication: initialization completed in %d ms", complete_time - start_time)

with app.app_context():
    from App.Server import controller

    _ = controller


def startup():
    logging.info("Using environment [%s]", app.config['ENV'])
    logging.info("Flask start with port [%d] (http) on [%s]", port, host)
    if app.config['ENV'] == "production":
        make_server(
            host=host,
            port=port,
            app=app
        ).serve_forever()
        app.run()

    else:
        app.run(
            host=host,
            port=port,
            debug=True
        )


if True:
    from App.Server.service import reset

    start_time = time.time() * 1000
    logging.info("Initializing Cache...")
    reset()
    complete_time = time.time() * 1000
    logging.info("Cache: initialization completed in %d ms", complete_time - start_time)
