#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _with_param.py
""""""
from ztxlib.rpbatis import InsertMany
from ztxlib.rpbatis import DeleteMany
from ztxlib.rpbatis import Update
from ztxlib.rpbatis import Select


@InsertMany("INSERT INTO `KCB`("
            "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`SFYXZX`"
            ") VALUES ("
            "#{JXLMC},#{jsmph},#{JASDM},#{SKZWS},#{zylxdm},#{jc_ks},#{jc_js},#{jyytms},#{kcm},#{day},#{SFYXZX}"
            ")")
def insert_into_kcb(*args: dict): pass


@Select("SELECT * FROM `JAS` WHERE JXLDM=#{jxldm}")
def get_jas_list_by_jxldm(jxldm: str): pass


@DeleteMany("DELETE FROM `dev` WHERE `day`=#{day} AND `JASDM`=#{JASDM} AND `jc_ks`=#{jc} AND `jc_js`=#{jc}")
def delete_incorrectness(*args: dict): pass


@Update("UPDATE `dev` SET "
        "`SKZWS`=#{skzws}, "
        "`zylxdm`=#{zylxdm}, "
        "`jc_ks`=#{jc_ks}, "
        "`jyytms`=#{jyytms}, "
        "`kcm`=#{kcm} WHERE "
        "`day`=#{day} AND "
        "`JASDM`=#{jasdm} AND "
        "`jc_ks`=#{jc_js} AND "
        "`jc_js`=#{jc_js}")
def update_incorrectness(skzws: int, zylxdm: str, jyytms: str, kcm: str,
                         day: str, jasdm: str, jc_ks: int, jc_js: int): pass


@Select("SELECT * FROM `dev` WHERE `JXLMC`=#{jxlmc} AND `day`=#{day} ORDER BY `jsmph`,`jc_js`")
def get_origin_by_jxlmc_and_day(jxlmc: str, day: str): pass


@InsertMany("INSERT INTO `dev`("
            "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,"
            "`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`SFYXZX`"
            ") VALUES ("
            "#{JXLMC},#{jsmph},#{JASDM},#{SKZWS},#{zylxdm},#{jc_ks},#{jc_js},#{jyytms},#{kcm},#{day},#{SFYXZX}"
            ")")
def insert_into_dev(*data_list: dict): pass
