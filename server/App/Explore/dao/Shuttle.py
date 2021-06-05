#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
from ztxlib.rpbatis import Select


@Select("SELECT * FROM `shuttle` WHERE (`working`& #{day}) AND `route`=#{route}")
def get_shuttles(day: int, route: int): pass
