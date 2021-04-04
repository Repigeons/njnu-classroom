#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Select.py
""""""
import json
import logging

from ._connections import connections


def select(sql: str):
    def func(_):
        def f(**kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql % kwargs, kwargs)
                if len(kwargs):
                    logging.info(
                        "Submit [%s] with parameter:\n%s",
                        cursor.statement,
                        json.dumps(kwargs, ensure_ascii=False)
                    )
                else:
                    logging.info("Submit [%s]", cursor.statement)
                return cursor.fetchall()
            finally:
                cursor.close(), connection.close()

        return f

    return func
