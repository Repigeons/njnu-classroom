#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/11 0011
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  service.py
""""""
import logging
import os
import time
from wsgiref.simple_server import make_server

from flask import Flask

from utils.aop import configuration


@configuration("application.explore.host")
def host(): pass


@configuration("application.explore.port")
def port(): pass


start_time = time.time() * 1000
logging.info("Initializing FlaskApplication...")
app = Flask(__name__)
complete_time = time.time() * 1000
logging.info("FlaskApplication: initialization completed in %d ms", complete_time - start_time)

with app.app_context():
    from App.Explore import controller

    _ = controller


def startup():
    logging.info("Using environment [%s]", app.config['ENV'])
    logging.info("Flask start with port [%d] (http) on [%s]", port, host)
    logging.info("Started Application in %f seconds", (int(time.time() * 1000) - int(os.getenv("startup_time"))) / 1000)
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
