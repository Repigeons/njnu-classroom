#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import logging
from wsgiref.simple_server import make_server
from flask.logging import default_handler

from .app import app


def main():
    host = app.config['host'] if 'host' in app.config else "localhost"
    port = app.config['port'] if 'port' in app.config else 8000
    logger = app.config['logger'] if 'logger' in app.config else None
    if app.config['ENV'] == "production":
        app.logger.addHandler(default_handler)
        if logger is not None:
            logger_handler = logging.FileHandler(logger)
            logger_handler.setLevel(logging.INFO)
            app.logger.addHandler(logger_handler)

        make_server(host=host, port=port, app=app).serve_forever()
        app.run()

    else:
        app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    main()
