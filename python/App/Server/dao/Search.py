#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Search.py
""""""
from utils.repdbanno import select


@select("SELECT * FROM `pro` WHERE (%s) AND (%s) AND (%s) AND (%s) AND (%s)" %
        ('%(_day)s', '%(_jc)s', '%(_jxl)s', '%(_zylxdm)s', '%(_keyword)s'))
def search(_day: str, _jc: str, _jxl: str, _zylxdm: str, _keyword: str, **kwargs):
    _ = _day, _jc, _jxl, _zylxdm, _keyword, kwargs
