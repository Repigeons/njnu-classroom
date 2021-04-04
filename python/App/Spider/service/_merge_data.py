#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/1/10 0010
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _merge_data.py
""""""
import json

from redis import StrictRedis

from App.Spider import dao
from utils.aop import autowired


@autowired()
def redis_pool(): pass


def merge() -> None:
    """
    将`dev`表中连续的空教室记录合并为单条记录
    """
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    redis = StrictRedis(connection_pool=redis_pool)
    jxl_list = [jxl.JXLMC for jxl in dao.get_distinct_jxl_in_dev()]
    # 全部缓存到redis
    for jxl in jxl_list:
        print("开始下载：", jxl, "...")
        jxl_classrooms = []
        for day in days:
            classrooms = []
            rows = dao.get_origin_by_jxlmc_and_day(jxlmc=jxl, day=day)
            for row in rows:
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
    dao.truncate_dev()
    # 重新插入数据库
    for jxl in jxl_list:
        dao.insert_into_dev(*json.loads(redis.hget("Spider", jxl)))
        print("归并完成：", jxl)
