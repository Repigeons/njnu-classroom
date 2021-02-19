#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/11 0011
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import logging
import os
import time
from wsgiref.simple_server import make_server

import App.Explore._ApplicationContext as Context
from App.Explore._ApplicationContext import send_email

from App.Explore.app import app


def main():
    try:
        logging.info("Using environment [%s]", app.config['ENV'])
        logging.info("Flask started with port [%d] (http) on [%s]", Context.port, Context.host)
        now = time.time() * 1000
        logging.info(
            "Started Application in %f seconds",
            (int(now) - int(os.getenv("startup_time"))) / 1000
        )
        if app.config['ENV'] == "production":
            make_server(
                host=Context.host,
                port=Context.port,
                app=app
            ).serve_forever()
            app.run()

        else:
            app.run(
                host=Context.host,
                port=Context.port,
                app=app,
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
