#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/11 0011
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import logging

from utils.aop import autowired


@autowired()
def send_email(subject: str, message: str): _ = subject, message


def main():
    try:
        from App.Explore import app
        app.startup()

    except KeyboardInterrupt as e:
        raise e

    except Exception as e:
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.error(f"{type(e), e}")
        logging.info("Exit with code %d", -1)
        exit(-1)


if __name__ == '__main__':
    main()
