#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
import logging
from email.mime.text import MIMEText

from app import app
from orm import JAS
from ztxlib import *


async def save_classrooms():
    """
    将教学楼及教室信息保存至Redis
    """
    try:
        logging.info("开始查询教学楼及教室信息...")
        classrooms = await get_classrooms()
        logging.info("教学楼及教室信息查询成功")
        async with aioredis.start(app['redis']) as redis:
            await redis.hset("spider", "classrooms", json.dumps(classrooms))
        logging.info("教学楼及教室信息存储完成")

    except Exception as e:
        async with app['smtp'] as smtp:
            await smtp.send(
                **app['mail'],
                subject="【南师教室】错误报告",
                mime_parts=[MIMEText(
                    f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
                )])
        logging.critical(f"{type(e), e}")
        logging.info("Exit with code %d", -1)
        exit(-1)


async def get_classrooms() -> dict[str, list[dict]]:
    """
    获取教室列表
    :return: {教学楼:[{教室信息}]}
    """
    mysql: aiomysql.MySQL = app['mysql']
    result = {}
    res = await mysql.fetchall("SELECT DISTINCT `JXLDM`,`JXLDM_DISPLAY` FROM `JAS`")
    jxl_list = [(row['JXLDM'], row['JXLDM_DISPLAY']) for row in res]
    for jxldm, jxlmc in jxl_list:
        res = await mysql.fetchall(
            "SELECT * FROM `JAS` WHERE JXLDM=%(jxldm)s",
            dict(jxldm=jxldm)
        )
        jas_list = [JAS(row) for row in res]
        jas_list.sort(key=lambda item: item.jsmph)
        result[jxlmc] = [item.json for item in jas_list]
    return result
