#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
from ztxlib.rpbatis import Insert
from ztxlib.rpbatis import Select


@Insert("INSERT INTO `feedback_metadata` (jc, JASDM) VALUES (#{jc}, #{jasdm})")
def add_feedback(jc: str, jasdm: str): pass


@Select("SELECT DATE_FORMAT(`feedback_metadata`.`time`, '%%Y-%%m-%%d') `date`, COUNT(*) `count` "
        "FROM `feedback_metadata` "
        "WHERE `JASDM`=#{jasdm} "
        "AND DAYOFWEEK(`feedback_metadata`.`time`)-1=#{day} "
        "AND `jc`=#{jc} "
        "GROUP BY `date` "
        "ORDER BY `date`")
def get_feedback(jasdm: str, day: int, jc: str): pass


@insert("INSERT INTO `correction` ("
        "day, JXLMC, jsmph, JASDM, jc_ks, jc_js, jyytms, kcm"
        ") VALUES ("
        "%s, %s, %s, %s,  %s, %s, '占用','####占用')" %
        ('%%(day)s', '%%(jxlmc)s', '%%(jsmph)s', '%%(jasdm)s', '%%(jc)s', '%%(jc)s'))
def add_correction(day: str, jxlmc: str, jsmph: str, jasdm: str, jc: str): _ = day, jxlmc, jsmph, jasdm, jc
