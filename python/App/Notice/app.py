#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import logging
import os
import time
from wsgiref.simple_server import make_server

from flask import Flask
from ztxlib.rpspring import Value


class __Application:
    @Value("application.notice.host")
    def host(self) -> str: pass

    @Value("application.notice.port")
    def port(self) -> int: pass


start_time = time.time() * 1000
logging.info("Initializing FlaskApplication...")
app = Flask(__name__)
complete_time = time.time() * 1000
logging.info("FlaskApplication: initialization completed in %d ms", complete_time - start_time)

with app.app_context():
    from . import controller

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
