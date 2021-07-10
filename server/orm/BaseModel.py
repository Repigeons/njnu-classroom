#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from abc import abstractmethod


class BaseModel:
    __abstract__ = True

    @abstractmethod
    def __init__(self, row: dict): pass

    @abstractmethod
    def json(self) -> dict: pass
