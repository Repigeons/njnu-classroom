#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Select.py
""""""
import logging

from ._connections import connections


def select(sql: str):
    def func(_):
        def f(**kwargs):
            logging.info(f"Submit sql sentence [{sql % kwargs}] with param:\n{kwargs}")
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql % kwargs, kwargs)
                return cursor.fetchall()
            finally:
                cursor.close(), connection.close()

        return f

    return func
