#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Update.py
""""""
from ._connections import connections


def update(sql: str):
    def func(_):
        def f(**kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql % kwargs, kwargs)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func


def update_many(sql: str):
    def func(_):
        def f(*args: dict, **kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql % kwargs, args)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func
