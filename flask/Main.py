#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/20 0020
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Main.py
""""""
import logging
from wsgiref.simple_server import make_server

from flask.logging import default_handler

from app import app, env


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-host', default='localhost', type=str, help='host to listen on')
    parser.add_argument('-port', default=8000, type=int, help='port to listen on')
    parser.add_argument('-logger', default=None, type=str, help='outputting log file')
    args = parser.parse_args()

    if env == 'dev':
        app.run(host=args.host, port=args.port, debug=True)
    else:
        app.logger.addHandler(default_handler)
        if args.logger is not None:
            logger_handler = logging.FileHandler(args.logger)
            app.logger.addHandler(logger_handler)

        make_server(host=args.host, port=args.port, app=app).serve_forever()
        app.run()


if __name__ == '__main__':
    main()
