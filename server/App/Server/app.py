#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  service.py
""""""
import logging
import os
import time
from wsgiref.simple_server import make_server

import flask.templating
from flask import Flask

from ztxlib.rpspring import Bean
from ztxlib.rpspring import Value


@Bean
def day_mapper():
    return {
        0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday',
        'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6,
    }


class __Application:
    @Value("application.server.host")
    def host(self): pass

    @Value("application.server.port")
    def port(self): pass


start_time = time.time() * 1000
logging.info("Initializing FlaskApplication...")
app = Flask(__name__)
complete_time = time.time() * 1000
logging.info("FlaskApplication: initialization completed in %d ms", complete_time - start_time)

with app.app_context():
    from App.Server import controller

    _ = controller


def startup():
    logging.info("Using environment [%s]", app.env)
    logging.info("Flask start with port [%d] (http) on [%s]", __Application.port, __Application.host)
    logging.info("Started Application in %f seconds", (int(time.time() * 1000) - int(os.getenv("startup_time"))) / 1000)
    if app.env == "production":
        make_server(
            host=__Application.host,
            port=__Application.port,
            app=app
        ).serve_forever()
        app.run()

    else:
        app.run(
            host=__Application.host,
            port=__Application.port,
            debug=True
        )


if True:
    from App.Server.service import reset

    start_time = time.time() * 1000
    logging.info("Initializing Cache...")
    reset()
    complete_time = time.time() * 1000
    logging.info("Cache: initialization completed in %d ms", complete_time - start_time)
