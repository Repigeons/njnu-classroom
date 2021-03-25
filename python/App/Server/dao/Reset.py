#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Reset.py
""""""
from utils.repdbanno import select


@select("SELECT DISTINCT `JXLDM_DISPLAY` FROM `JAS` WHERE `SFYXZX`")
def get_jxl_list(): pass


@select("SELECT * FROM `pro` "
        "WHERE `JXLMC`=%s AND `day`=%s AND `zylxdm` in ('00', '10') AND `SFYXZX` "
        "ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`" %
        ('%%(jxlmc)s', '%%(day)s'))
def get_empty_classroom(jxlmc: str, day: str): _ = jxlmc, day


@select("SELECT DISTINCT `JASDM` FROM `JAS`")
def get_jas_list(): pass


@select("SELECT * FROM `pro` WHERE `JASDM`=%s" %
        ('%%(jasdm)s',))
def get_overview_row(jasdm: str): _ = jasdm
