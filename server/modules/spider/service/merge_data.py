#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
import logging
from typing import List

from app import app
from orm.KCB import KCB
from ztxlib import *


async def merge():
    """
    将`dev`表中连续的空教室记录合并为单条记录
    """
    mysql: aiomysql.MySQL = app['mysql']
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    res = await mysql.fetchall("SELECT DISTINCT `JXLMC` FROM `dev`")
    jxl_list: List[str] = [row['JXLMC'] for row in res]
    # 全部缓存到redis
    for jxl in jxl_list:
        logging.info("[%s] Start merging...", jxl)
        jxl_classrooms = []
        for day in days:
            classrooms = []
            res = await mysql.fetchall(
                "SELECT * FROM `dev` WHERE `JXLMC`=%(jxlmc)s AND `day`=%(day)s ORDER BY `jsmph`,`jc_js`",
                dict(jxlmc=jxl, day=day)
            )
            rows = [KCB(row) for row in res]
            for row in rows:
                if len(classrooms) == 0:
                    classrooms.append(row)
                elif row.JASDM == classrooms[-1].JASDM and row.zylxdm == '00' and classrooms[-1].zylxdm == '00':
                    classrooms[-1].jc_js = row.jc_js
                else:
                    classrooms.append(row)
            jxl_classrooms.extend(classrooms)
        async with aioredis.start(app['redis']) as redis:
            await redis.hset("spider", jxl, json.dumps([item.json for item in jxl_classrooms]))
    # 清空数据库
    await mysql.execute("TRUNCATE TABLE `dev`")
    # 重新插入数据库
    for jxl in jxl_list:
        async with aioredis.start(app['redis']) as redis:
            args = json.loads(await redis.hget("spider", jxl))
            await mysql.execute(
                "INSERT INTO `dev`("
                "`JXLMC`, `jsmph`, `JASDM`, `SKZWS`, `zylxdm`, "
                "`jc_ks`, `jc_js`, `jyytms`, `kcm`, `day`, `SFYXZX`"
                ") VALUES ("
                "%(JXLMC)s, %(jsmph)s, %(JASDM)s, %(SKZWS)s, %(zylxdm)s, "
                "%(jc_ks)s, %(jc_js)s, %(jyytms)s, %(kcm)s, %(day)s, %(SFYXZX)s"
                ")",
                *args
            )
        logging.info("[%s] Merging completed...", jxl)
