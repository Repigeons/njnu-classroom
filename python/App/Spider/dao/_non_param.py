#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _non_param.py
""""""
from utils.repdbanno import insert, select


@insert("TRUNCATE TABLE `KCB`")
def truncate_kcb(): pass


@insert("TRUNCATE TABLE `dev`")
def truncate_dev(): pass


@insert("TRUNCATE TABLE `pro`")
def truncate_pro(): pass


@insert("INSERT INTO `dev` SELECT * FROM `KCB`")
def copy_kcb_to_dev(): pass


@insert("INSERT INTO `pro` SELECT * FROM `dev`")
def copy_dev_to_pro(): pass


@select("SELECT * FROM `correction`")
def get_correction(): pass


@select("SELECT DISTINCT `JXLDM`,`JXLDM_DISPLAY` FROM `JAS`")
def get_distinct_jxl_in_jas(): pass


@select("SELECT DISTINCT `JXLMC` FROM `dev`")
def get_distinct_jxl_in_dev(): pass
