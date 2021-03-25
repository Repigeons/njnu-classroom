#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _beans.py
""""""
import logging
import time

from ._storage import __beans


def bean(name: str = None):
    def func(f):
        _name = getattr(f, '__name__') if name is None else name
        if _name in __beans.keys():
            logging.warning(f"Bean '{_name}' has been registered.")
        start_time = time.time() * 1000
        __beans[_name] = f()
        complete_time = time.time() * 1000
        logging.info(f"Registered Bean {__beans[_name]} as '{_name}' in %d ms", complete_time - start_time)
        return f

    return func


def autowired(name: str = None, default=None):
    def func(f):
        _name = getattr(f, '__name__') if name is None else name
        if _name not in __beans.keys():
            logging.warning(f"Bean '{_name}' has not been registered.")
        return __beans[_name] if _name in __beans.keys() else default

    return func
