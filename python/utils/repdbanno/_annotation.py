#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _annotation.py
""""""
from ._connections import connections


def insert(sql: str):
    def func(_):
        def f(**kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql, kwargs)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func


def delete(sql: str):
    def func(_):
        def f(**kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql, kwargs)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func


def update(sql: str):
    def func(_):
        def f(**kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql, kwargs)
                return None
            finally:
                cursor.close(), connection.close()

        return f

    return func


def select(sql: str):
    def func(_):
        def f(**kwargs):
            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(sql, kwargs)
                return cursor.fetchall()
            finally:
                cursor.close(), connection.close()

        return f

    return func
