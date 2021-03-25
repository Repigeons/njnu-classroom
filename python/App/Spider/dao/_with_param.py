#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _with_param.py
""""""
from utils.repdbanno import insert_many, delete_many, update, select


@insert_many("INSERT INTO `KCB`("
             "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`SFYXZX`"
             ") VALUES ("
             "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
             ")" %
             ('%(JXLMC)s', '%(_jsmph)s', '%(_JASDM)s', '%(_SKZWS)s', '%(_zylxdm)s', '%(_jc_ks)s', '%(_jc_js)s',
              '%(_jyytms)s', '%(_kcm)s', '%(_day)s', '%(_SFYXZX)s'))
def insert_into_kcb(*args: dict): _ = args


@select("SELECT * FROM `JAS` WHERE JXLDM=%s" %
        ('%%(jxldm)s',))
def get_jas_list_by_jxldm(jxldm: str): _ = jxldm


@delete_many("DELETE FROM `dev` WHERE `day`=%s AND `JASDM`=%s AND `jc_ks`=%s AND `jc_js`=%s" %
             ('%%(day)s', '%%(JASDM)s', '%%(jc)s', '%%(jc)s'))
def delete_incorrectness(*args: dict): _ = args


@update("UPDATE `dev` SET "
        "`SKZWS`=%s, "
        "`zylxdm`=%s, "
        "`jc_ks`=%s, "
        "`jyytms`=%s, "
        "`kcm`=%s WHERE "
        "`day`=%s AND "
        "`JASDM`=%s AND "
        "`jc_ks`=%s AND "
        "`jc_js`=%s" %
        ('%%(skzws)s', '%%(zylxdm)s', '%%(jc_ks)s', '%%(jyytms)s',
         '%%(kcm)s', '%%(day)s', '%%(jasdm)s', '%%(jc_js)s', '%%(jc_js)s'))
def update_incorrectness(
        skzws: int, zylxdm: str, jyytms: str, kcm: str, day: str, jasdm: str, jc_ks: int, jc_js: int):
    _ = skzws, zylxdm, jyytms, kcm, day, jasdm, jc_ks, jc_js


@select("SELECT * FROM `dev` WHERE `JXLMC`=%s AND `day`=%s ORDER BY `jsmph`,`jc_js`" %
        ('%%(jxlmc)s', '%%(day)s'))
def get_origin_by_jxlmc_and_day(jxlmc: str, day: str): _ = jxlmc, day


@insert_many("INSERT INTO `dev`("
             "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,"
             "`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`SFYXZX`"
             ") VALUES ("
             "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
             ")" %
             ('%%(JXLMC)s', '%%(jsmph)s', '%%(JASDM)s', '%%(SKZWS)s', '%%(zylxdm)s', '%%(jc_ks)s',
              '%%(jc_js)s', '%%(jyytms)s', '%%(kcm)s', '%%(day)s', '%%(SFYXZX)s'))
def insert_into_dev(*data_list: dict): _ = data_list
