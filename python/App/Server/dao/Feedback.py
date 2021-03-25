#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
from utils.repdbanno import insert, select


@insert("INSERT INTO `feedback_metadata` (jc, JASDM) VALUES (%s, %s)" % ('%%(jc)s', '%%(jasdm)s'))
def add_feedback(jc: str, jasdm: str): _ = jc, jasdm


@select("SELECT DATE_FORMAT(`feedback_metadata`.`time`, '%%Y-%%m-%%d') `date`, COUNT(*) `count` "
        "FROM `feedback_metadata` "
        "WHERE `JASDM`=%s "
        "AND DAYOFWEEK(`feedback_metadata`.`time`)-1=%s "
        "AND `jc`=%s "
        "GROUP BY `date` "
        "ORDER BY `date`" %
        ('%%(jasdm)s', '%%(day)s', '%%(jc)s'))
def get_feedback(jasdm: str, day: int, jc: str): _ = jasdm, day, jc


@insert("INSERT INTO `correction` ("
        "day, JXLMC, jsmph, JASDM, jc_ks, jc_js, jyytms, kcm"
        ") VALUES ("
        "%s, %s, %s, %s,  %s, %s, '占用','####占用')" %
        ('%%(day)s', '%%(jxlmc)s', '%%(jsmph)s', '%%(jasdm)s', '%%(jc)s', '%%(jc)s'))
def add_correction(day: str, jxlmc: str, jsmph: str, jasdm: str, jc: str): _ = day, jxlmc, jsmph, jasdm, jc
