#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import logging

from ztxlib.rpspring import Autowired
from ztxlib.rpspring import Value


class __Application:
    @Autowired
    def send_email(self) -> None: pass

    @Value("application.explore.host")
    def host(self) -> str: pass

    @Value("application.explore.port")
    def port(self) -> int: pass


def main():
    try:
        from App.Notice import app
        app.startup()

    except KeyboardInterrupt as e:
        raise e

    except Exception as e:
        __Application.send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.error(f"{type(e), e}")
        logging.info("Exit with code %d", -1)
        exit(-1)
