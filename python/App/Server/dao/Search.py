#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Search.py
""""""
from ztxlib.rpbatis import Select


@Select("SELECT * FROM `pro` WHERE (${_day}) AND (${_jc}) AND (${_jxl}) AND (${_zylxdm}) AND (${_keyword})")
def search(_day: str, _jc: str, _jxl: str, _zylxdm: str, _keyword: str, **kwargs): pass
