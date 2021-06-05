#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Reset.py
""""""
import json

from redis import StrictRedis
from redis_lock import Lock
from ztxlib.rpspring import Autowired
from ztxlib.rpspring import Value

from App.Server import dao


class __Application:
    @Autowired
    def redis_pool(self): pass

    @Autowired
    def day_mapper(self) -> dict: pass

    @Value("application.server.service")
    def serve(self) -> bool: pass


def reset():
    redis = StrictRedis(connection_pool=__Application.redis_pool)
    lock1 = Lock(redis, "Server-Empty")
    lock2 = Lock(redis, "Server-Overview")
    if lock1.acquire(blocking=False):
        try:
            redis.delete("Empty")
            reset_empty()
        finally:
            lock1.release()
    if lock2.acquire(blocking=False):
        try:
            redis.delete("Overview")
            reset_overview()
        finally:
            lock2.release()


def reset_empty():
    redis = StrictRedis(connection_pool=__Application.redis_pool)
    jxl_list = dao.get_jxl_list()
    for jxl in jxl_list:
        jxlmc = jxl.JXLDM_DISPLAY
        for day in range(7):
            rows = dao.get_empty_classroom(jxlmc=jxlmc, day=__Application.day_mapper[day])
            redis.hset(
                name="Empty",
                key=f"{jxlmc}_{day}",
                value=json.dumps([
                    {
                        'JASDM': row.JASDM,
                        'jsmph': row.jsmph,  # 教室门牌号
                        'SKZWS': row.SKZWS,  # 上课座位数
                        'jc_ks': row.jc_ks,  # 开始节次
                        'jc_js': row.jc_js,  # 结束节次
                        'zylxdm': row.zylxdm,  # 资源类型代码
                    } for row in rows
                ])
            )


def reset_overview():
    redis = StrictRedis(connection_pool=__Application.redis_pool)
    jas_list = dao.get_jas_list()
    for jas in jas_list:
        rows = dao.get_overview_row(jasdm=jas.JASDM)
        redis.hset(
            name="Overview",
            key=jas.JASDM,
            value=json.dumps([
                {
                    'JXLMC': row.JXLMC,
                    'jsmph': row.jsmph,
                    'SKZWS': row.SKZWS,

                    'day': __Application.day_mapper[row.day],
                    'jc_ks': row.jc_ks,
                    'jc_js': row.jc_js,

                    'zylxdm': row.zylxdm,
                    'jyytms': row.jyytms,
                    'kcm': row.kcm,
                } for row in rows
            ])
        )
