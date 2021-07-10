#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from orm.BaseModel import BaseModel


class Shuttle(BaseModel):
    def __init__(self):
        pass

    @property
    def json(self) -> dict:
        return dict()
