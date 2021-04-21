#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Reset.py
""""""
from ztxlib.rpbatis import Select


@Select("SELECT DISTINCT `JXLDM_DISPLAY` FROM `JAS` WHERE `SFYXZX`")
def get_jxl_list(): pass


@Select("SELECT * FROM `pro` "
        "WHERE `JXLMC`=#{jxlmc} AND `day`=#{day} AND `zylxdm` in ('00', '10') AND `SFYXZX` "
        "ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`")
def get_empty_classroom(jxlmc: str, day: str): pass


@Select("SELECT DISTINCT `JASDM` FROM `JAS`")
def get_jas_list(): pass


@Select("SELECT * FROM `pro` WHERE `JASDM`=#{jasdm}")
def get_overview_row(jasdm: str): pass
