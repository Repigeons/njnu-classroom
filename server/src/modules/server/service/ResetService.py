#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import json

from app import app
from ztxlib import *
from .static import day_mapper


def reset():
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
                for day in range(7)
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


async def reset_empty_once(jxlmc: str, day: int):
    mysql: aiomysql.MySQL = app['mysql']
    rows = await mysql.fetchall(
        "SELECT * FROM `pro` "
        "WHERE `JXLMC`=%(jxlmc)s AND `day`=%(day)s AND `zylxdm` in ('00', '10') AND `SFYXZX` "
        "ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`",
        dict(
            jxlmc=jxlmc,
            day=day_mapper[day],
        )
    )
    async with aioredis.start(app['redis']) as redis:
        await redis.hset(
            name="empty",
            key=f"{jxlmc}_{day}",
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
        "SELECT * FROM `pro` WHERE `JASDM`=%(jasdm)s",
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

                    day=day_mapper[row['day']],
                    jc_ks=row['jc_ks'],
                    jc_js=row['jc_js'],

                    zylxdm=row['zylxdm'],
                    jyytms=row['jyytms'],
                    kcm=row['kcm'],
                ) for row in rows
            ])
        )
