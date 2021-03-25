#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/1/10 0010
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _correct_data.py
""""""
from utils.aop import autowired


@autowired()
def mysql(): pass


def correct() -> None:
    """
    从`correction`表读取数据，依此对`dev`表进行校正
    """
    connection, cursor = mysql.get_connection_cursor()
    print("待校正数据：")
    cursor.execute("SELECT * FROM `correction`")
    correction_list = cursor.fetchall()
    for correction in correction_list:
        print([
            correction.day, correction.jc_ks, correction.jc_js,
            correction.JXLMC, correction.jsmph,
            correction.zylxdm, correction.jyytms, correction.kcm
        ])
        data = [
            {'day': correction.day, 'JASDM': correction.JASDM, 'jc': jc}
            for jc in range(correction.jc_ks, correction.jc_js)
        ]
        if len(data) > 0:
            cursor.executemany(
                "DELETE FROM `dev` WHERE `day`=%(day)s AND `JASDM`=%(JASDM)s AND `jc_ks`=%(jc)s AND `jc_js`=%(jc)s",
                data
            )
        cursor.execute(
            "UPDATE `dev` SET "
            "`SKZWS`=%(SKZWS)s, "
            "`zylxdm`=%(zylxdm)s, "
            "`jc_ks`=%(jc_ks)s, "
            "`jyytms`=%(jyytms)s, "
            "`kcm`=%(kcm)s WHERE "
            "`day`=%(day)s AND "
            "`JASDM`=%(JASDM)s AND "
            "`jc_ks`=%(jc_js)s AND "
            "`jc_js`=%(jc_js)s",
            {
                'SKZWS': correction.SKZWS,
                'zylxdm': correction.zylxdm,
                'jc_ks': correction.jc_ks,
                'jc_js': correction.jc_js,
                'jyytms': correction.jyytms,
                'kcm': correction.kcm,
                'day': correction.day,
                'JASDM': correction.JASDM
            }
        )
    cursor.close(), connection.close()


def copy_to_dev() -> None:
    """
    将原始课程数据从`KCB`表复制到`dev`表，待后续处理
    """
    connection, cursor = mysql.get_connection_cursor()
    cursor.execute("TRUNCATE TABLE `dev`")
    cursor.execute("INSERT INTO `dev` SELECT * FROM `KCB`")
    cursor.close(), connection.close()


def copy_to_pro() -> None:
    """
    将课程数据从`dev`表复制到`pro`表，用于生产环境
    """
    connection, cursor = mysql.get_connection_cursor()
    cursor.execute("TRUNCATE TABLE `pro`")
    cursor.execute("INSERT INTO `pro` SELECT * FROM `dev`")
    cursor.close(), connection.close()
