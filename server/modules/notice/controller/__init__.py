#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from .middlewares import middlewares
from .routes import routes

from . import IndexController

__all__ = (
    'middlewares',
    'routes',
)
