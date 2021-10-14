#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import json
import os

from app import app
from ztxlib import *

env: str


def reset():
    global env
    env = os.getenv('env', 'dev')
    env = 'pro' if env == 'pro' else 'dev'
    return asyncio.gather(
        reset_empty(),
        reset_overview(),
    )


async def reset_empty():
    mysql: aiomysql.MySQL = app['mysql']
    jxl_list = await mysql.fetchall("SELECT DISTINCT `JXLDM_DISPLAY` AS `JXLMC` FROM `JAS` WHERE `SFYXZX`")
    jxl_list = [jxl['JXLMC'] for jxl in jxl_list]
    try:
        async with aioredis.lock(app['redis'], 'reset-empty', 0):
            async with aioredis.start(app['redis']) as redis:
                await redis.delete('empty')
            await asyncio.gather(*[
                reset_empty_once(jxlmc, day)
                for jxlmc in jxl_list
                for day in ['Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.']
            ])
    except aioredis.exceptions.WaitingTimeoutError:
        pass


async def reset_overview():
    mysql: aiomysql.MySQL = app['mysql']
    jas_list = await mysql.fetchall("SELECT DISTINCT `JASDM` FROM `JAS`")
    jas_list = [jas['JASDM'] for jas in jas_list]
    try:
        async with aioredis.lock(app['redis'], 'reset-overview', 0):
            async with aioredis.start(app['redis']) as redis:
                await redis.delete('overview')
            await asyncio.gather(*[
                reset_overview_once(jasdm)
                for jasdm in jas_list
            ])
    except aioredis.exceptions.WaitingTimeoutError:
        pass


async def reset_empty_once(jxlmc: str, day: str):
    mysql: aiomysql.MySQL = app['mysql']
    rows = await mysql.fetchall(
        f"SELECT * FROM `{env}` "
        "WHERE `JXLMC`=%(jxlmc)s AND `day`=%(day)s AND `zylxdm` in ('00', '10') AND `SFYXZX` "
        "ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`",
        dict(
            jxlmc=jxlmc,
            day=day,
        )
    )
    async with aioredis.start(app['redis']) as redis:
        await redis.hset(
            name="empty",
            key=f"{jxlmc}:{day}",
            value=json.dumps([
                dict(
                    JASDM=row['JASDM'],
                    jsmph=row['jsmph'],  # 教室门牌号
                    SKZWS=row['SKZWS'],  # 上课座位数
                    jc_ks=row['jc_ks'],  # 开始节次
                    jc_js=row['jc_js'],  # 结束节次
                    zylxdm=row['zylxdm'],  # 资源类型代码
                ) for row in rows
            ])
        )


async def reset_overview_once(jasdm: str):
    mysql: aiomysql.MySQL = app['mysql']
    rows = await mysql.fetchall(
        f"SELECT * FROM `{env}` WHERE `JASDM`=%(jasdm)s",
        dict(
            jasdm=jasdm
        )
    )
    async with aioredis.start(app['redis']) as redis:
        await redis.hset(
            name="overview",
            key=jasdm,
            value=json.dumps([
                dict(
                    JXLMC=row['JXLMC'],
                    jsmph=row['jsmph'],
                    SKZWS=row['SKZWS'],

                    day=row['day'],
                    jc_ks=row['jc_ks'],
                    jc_js=row['jc_js'],

                    zylxdm=row['zylxdm'],
                    jyytms=row['jyytms'],
                    kcm=row['kcm'],
                ) for row in rows
            ])
        )
