#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
from utils.repdbanno import select


@select("SELECT * FROM `shuttle` WHERE (`working`& %s) AND `route`= %s" % ('%%(day)s', '%%(route)s'))
def get_shuttles(day: int, route: int): _ = day, route
