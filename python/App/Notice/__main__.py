#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
from wsgiref.simple_server import make_server

from App.Notice.app import app


def main():
    host = app.config['host'] if 'host' in app.config else "localhost"
    port = app.config['port'] if 'port' in app.config else 8000

    if app.config['ENV'] == "production":
        make_server(host=host, port=port, app=app).serve_forever()
        app.run()

    else:
        app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    main()
