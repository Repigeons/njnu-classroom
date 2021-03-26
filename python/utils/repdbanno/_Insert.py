#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Insert.py
""""""
import logging

from ._connections import connections


def insert(sql: str):
    def func(_):
        def f(**kwargs):
            logging.info(f"Submit sql sentence [{sql % kwargs}] with param:\n{kwargs}")
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql % kwargs, kwargs)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func


def insert_many(sql: str):
    def func(_):
        def f(*args: dict, **kwargs):
            logging.info(
                f"Submit sql sentence [{sql % kwargs}] with param:\n%s",
                '\n'.join([str(param) for param in args])
            )
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.executemany(sql % kwargs, args)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func
