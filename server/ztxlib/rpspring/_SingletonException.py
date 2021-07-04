#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _SingletonException
""""""


class SingletonException(Exception):
    def __init__(self, cls):
        if not isinstance(cls, str):
            cls = cls.__name__
        super().__init__(f"<class '{cls}'> is a singleton.")
