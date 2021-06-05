#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _non_param.py
""""""
from ztxlib.rpbatis import Insert
from ztxlib.rpbatis import Select


@Insert("TRUNCATE TABLE `KCB`")
def truncate_kcb(): pass


@Insert("TRUNCATE TABLE `dev`")
def truncate_dev(): pass


@Insert("TRUNCATE TABLE `pro`")
def truncate_pro(): pass


@Insert("INSERT INTO `dev` SELECT * FROM `KCB`")
def copy_kcb_to_dev(): pass


@Insert("INSERT INTO `pro` SELECT * FROM `dev`")
def copy_dev_to_pro(): pass


@Select("SELECT * FROM `correction`")
def get_correction(): pass


@Select("SELECT DISTINCT `JXLDM`,`JXLDM_DISPLAY` FROM `JAS`")
def get_distinct_jxl_in_jas(): pass


@Select("SELECT DISTINCT `JXLMC` FROM `dev`")
def get_distinct_jxl_in_dev(): pass
