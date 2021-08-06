#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from .MySQL import MySQL

create_pool = MySQL.create_pool

__all__ = (
    'MySQL',
    'create_pool',
)
