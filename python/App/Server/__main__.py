#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import logging
import os
import time
from wsgiref.simple_server import make_server

from utils.aop import autowired, configuration
from App.Server.app import app


@autowired()
def send_email(subject: str, message: str): _ = subject, message


@configuration("application.explore.host")
def host(): pass


@configuration("application.explore.port")
def port(): pass


def main():
    try:
        logging.info("Using environment [%s]", app.config['ENV'])
        logging.info("Flask started with port [%d] (http) on [%s]", port, host)
        now = time.time() * 1000
        logging.info(
            "Started Application in %f seconds",
            (int(now) - int(os.getenv("startup_time"))) / 1000
        )
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

    except KeyboardInterrupt as e:
        raise e

    except Exception as e:
        logging.error(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", -1)
        exit(-1)


if __name__ == '__main__':
    main()
