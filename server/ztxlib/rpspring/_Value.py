#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Value
""""""
from ._Context import ApplicationContext


class Value:
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __call__(self, _):
        if not isinstance(self.name, str):
            return self.name
        return ApplicationContext.get_configuration(self.name)

    def __get__(self, obj=None, objtype=None):
        if not isinstance(self.name, str):
            return self.name
        return ApplicationContext.get_configuration(self.name)
