#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/1/10 0010
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _merge_data.py
""""""
import json

from redis import StrictRedis
from utils.aop import autowired


@autowired()
def mysql(): pass


@autowired()
def redis_pool(): pass


def merge() -> None:
    """
    将`dev`表中连续的空教室记录合并为单条记录
    """
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    redis = StrictRedis(connection_pool=redis_pool)
    connection, cursor = mysql.get_connection_cursor()
    cursor.execute("SELECT DISTINCT `JXLMC` FROM `dev`")
    jxl_list = [jxl.JXLMC for jxl in cursor.fetchall()]
    # 全部保存到文件
    for jxl in jxl_list:
        print("开始下载：", jxl, "...")
        jxl_classrooms = []
        for day in days:
            classrooms = []
            cursor.execute(
                "SELECT * FROM `dev` WHERE `JXLMC`=%(JXLMC)s AND `day`=%(day)s ORDER BY `jsmph`,`jc_js`",
                {'JXLMC': jxl, 'day': day}
            )
            for row in cursor.fetchall():
                item = {
                    'id': row.id,
                    'JXLMC': row.JXLMC,
                    'jsmph': row.jsmph,
                    'JASDM': row.JASDM,
                    'SKZWS': row.SKZWS,
                    'zylxdm': row.zylxdm,
                    'jc_ks': row.jc_ks,
                    'jc_js': row.jc_js,
                    'jyytms': row.jyytms,
                    'kcm': row.kcm,
                    'day': row.day,
                    'SFYXZX': row.SFYXZX == b'\x01',
                }
                if len(classrooms) == 0:
                    classrooms.append(item)
                elif item['JASDM'] == classrooms[-1]['JASDM'] and \
                        item['zylxdm'] == '00' and classrooms[-1]['zylxdm'] == '00':
                    classrooms[-1]['jc_js'] = item['jc_js']
                else:
                    classrooms.append(item)
            jxl_classrooms.extend(classrooms)
        redis.hset("Spider", jxl, json.dumps(jxl_classrooms))
    # 清空数据库
    cursor.execute("TRUNCATE TABLE `dev`")
    # 重新插入数据库
    for jxl in jxl_list:
        cursor.executemany(
            "INSERT INTO `dev`("
            "`JXLMC`,`jsmph`,`JASDM`,`SKZWS`,`zylxdm`,"
            "`jc_ks`,`jc_js`,`jyytms`,`kcm`,`day`,`SFYXZX`"
            ") VALUES ("
            "%(JXLMC)s,%(jsmph)s,%(JASDM)s,%(SKZWS)s,%(zylxdm)s,"
            "%(jc_ks)s,%(jc_js)s,%(jyytms)s,%(kcm)s,%(day)s,%(SFYXZX)s"
            ")",
            json.loads(redis.hget("Spider", jxl))
        )
        print("归并完成：", jxl)
    cursor.close(), connection.close()
