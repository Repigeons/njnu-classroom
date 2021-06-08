#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_classrooms.py
""""""
import json
import logging
from typing import Dict, List

from redis import StrictRedis
from ztxlib.rpspring import Autowired

from App.Spider import dao


class __Application:
    @Autowired
    def redis_pool(self): pass

    @Autowired
    def send_email(self) -> None: pass


def save_classrooms() -> None:
    """
    将教学楼及教室信息保存至Redis
    """
    try:
        redis = StrictRedis(connection_pool=__Application.redis_pool)
        logging.info("开始查询教学楼及教室信息...")
        classrooms = get_classrooms()
        logging.info("教学楼及教室信息查询成功")
        redis.hset("Spider", "classrooms", json.dumps(classrooms))
        logging.info("教学楼及教室信息存储完成")
    except Exception as e:
        logging.error(f"{type(e), e}")
        __Application.send_email(
            subject="【南师教室】错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", -1)
        exit(-1)


def get_classrooms() -> Dict[str, List[dict]]:
    """
    获取教室列表
    :return: {教学楼:[{教室信息}]}
    """
    result = {}
    jxl_list = dao.get_distinct_jxl_in_jas()
    for jxl in jxl_list:
        result[jxl.JXLDM_DISPLAY] = []
        jas_list = dao.get_jas_list_by_jxldm(jxldm=jxl.JXLDM)
        for jas in jas_list:
            result[jxl.JXLDM_DISPLAY].append({
                'JXLMC': jas.JXLDM_DISPLAY,
                'JASMC': jas.JASMC,
                'JASDM': jas.JASDM,
                'SKZWS': jas.SKZWS,
                'SFYXZX': jas.SFYXZX == b'\x01',
                'jsmph': jas.JASMC.replace(jas.JXLDM_DISPLAY, '')
            })
        result[jxl.JXLDM_DISPLAY].sort(key=lambda item: item['jsmph'])
    return result
