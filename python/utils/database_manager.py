#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  database_manager.py
""""""
import json
from typing import Dict, List

from pymysql import DatabaseError

from ._mysql import MySQL

__db_config = json.load(open('conf/database.json'))
__database = MySQL(**__db_config['dev'])
if not __database.test_connection():
    print('数据库连接失败')
    print('Exit with code', 4)
    exit(4)


def set_env(env: str = "dev"):
    global __database
    __database = MySQL(**__db_config[env if env == 'pro' else 'dev'])
    if not __database.test_connection():
        print('数据库连接失败')
        print('Exit with code', 4)
        exit(4)


def truncate_kcb():
    __database.update("TRUNCATE TABLE `KCB`")


def get_classrooms() -> Dict[str, List[dict]]:
    """
    获取教室列表
    :return: {教学楼:[{教室信息},],}
    """
    result = {}
    jxl_list = __database.fetchall("SELECT DISTINCT `JXLDM`,`JXLDM_DISPLAY` FROM `JAS`")
    for jxl in jxl_list:
        result[jxl['JXLDM_DISPLAY']] = []
        jas_list = __database.fetchall("SELECT * FROM `JAS` WHERE JXLDM=%s", jxl['JXLDM'])
        for jas in jas_list:
            result[jxl['JXLDM_DISPLAY']].append({
                'JXLMC': jas['JXLDM_DISPLAY'],
                'JASMC': jas['JASMC'],
                'JASDM': jas['JASDM'],
                'SKZWS': jas['SKZWS'],
                'sfyxzx': jas['_SFYXZX'] == b'\x01',
                'jsmph': jas['JASMC'].replace(jas['JXLDM_DISPLAY'], '')
            })
        result[jxl['JXLDM_DISPLAY']].sort(key=lambda item: item['jsmph'])
    return result


def insert_into_kcb(class_list: list) -> None:
    __database.update_batch(*[(
        "INSERT INTO `KCB`("
        "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`_SFYXZX`"
        ") VALUES ("
        "%(JXLMC)s,%(jsmph)s,%(JASDM)s,%(SKZWS)s,%(zylxdm)s,%(jc_ks)s,%(jc_js)s,%(jyytms)s,%(kcm)s,%(day)s,%(sfyxzx)s"
        ");", row
    ) for row in class_list
    ])


def correct():
    for correction in __database.fetchall("SELECT * FROM `correction`"):
        print([
            correction['day'], correction['jc_ks'], correction['jc_js'],
            correction['JXLMC'], correction['jsmph'],
            correction['zylxdm'], correction['jyytms'], correction['kcm']
        ])
        sql = [(
            "DELETE FROM `dev` WHERE `day`=%(day)s AND `JASDM`=%(JASDM)s AND `jc_ks`=%(jc)s AND `jc_js`=%(jc)s",
            {'day': correction['day'], 'JASDM': correction['JASDM'], 'jc': jc}
        ) for jc in range(correction['jc_ks'], correction['jc_js'])
        ]
        sql.append((
            "UPDATE `dev` SET "
            "`SKZWS`=%(SKZWS)s, `jyytms`=%(jyytms)s, `kcm`=%(kcm)s WHERE "
            "`day`=%(day)s AND `JASDM`=%(JASDM)s AND `jc_ks`=%(jc_js)s AND `jc_js`=%(jc_js)s",
            correction))
        __database.update_batch(*sql)


def merge(temp_dir: str):
    jxl_list = __database.fetchall("SELECT DISTINCT `JXLMC` FROM `dev`")
    jxl_list = [jxl['JXLMC'] for jxl in jxl_list]
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    # 全部保存到文件
    for jxl in jxl_list:
        print("开始下载教学楼：", jxl)
        jxl_classrooms = []
        for day in days:
            classrooms = __database.fetchall(
                sql="SELECT * FROM `dev` WHERE `JXLMC`=%(JXLMC)s AND `day`=%(day)s ORDER BY `jsmph`,`jc_js`",
                args={'JXLMC': jxl, 'day': day}
            )
            classrooms2 = []
            for classroom in classrooms:
                classroom.pop(11)
                classroom['_SFYXZX'] = classroom['_SFYXZX'] == b'\x01'
                if len(classrooms2) == 0:
                    classrooms2.append(classroom)
                elif classroom['JASDM'] == classrooms2[-1]['JASDM'] and \
                        classroom['zylxdm'] == '00' and classrooms2[-1]['zylxdm'] == '00':
                    classrooms2[-1]['jc_js'] = classroom['jc_js']
                else:
                    classrooms2.append(classroom)
            jxl_classrooms.extend(classrooms2)
        json.dump(jxl_classrooms, open(f"{temp_dir}/jxl_classrooms_{jxl}.json", 'w', encoding='utf8'))
        print(jxl, "下载完成...")
    # 清空数据库
    __database.update("TRUNCATE TABLE `dev`")
    # 重新插入数据库
    for jxl in jxl_list:
        jxl_classrooms = json.load(open(f"{temp_dir}/jxl_classrooms_{jxl}.json", encoding='utf8'))
        __database.update_batch(*[(
            "INSERT INTO `dev`("
            "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,"
            "`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`_SFYXZX`"
            ") VALUES ("
            "%(JXLMC)s,%(jsmph)s,%(JASDM)s,%(SKZWS)s,%(zylxdm)s,"
            "%(jc_ks)s,%(jc_js)s,%(jyytms)s,%(kcm)s,%(day)s,%(_SFYXZX)s"
            ");", row
        ) for row in jxl_classrooms
        ])


def copy_to_dev():
    __database.update("TRUNCATE TABLE `dev`")
    __database.update("INSERT INTO `dev` SELECT * FROM `KCB`")


def copy_to_pro():
    __database.update("TRUNCATE TABLE `pro`")
    __database.update("INSERT INTO `pro` SELECT null, "
                      "`JXLMC`, `jsmph`, `JASDM`, `SKZWS`, "
                      "`zylxdm`, `jc_ks`, `jc_js`, `jyytms`, `kcm`, `day`, `_SFYXZX` "
                      "FROM `KCB`")
