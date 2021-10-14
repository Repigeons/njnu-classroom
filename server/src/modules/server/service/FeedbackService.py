#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
from multiprocessing import Process

import aiohttp

from app import app
from ztxlib import *
from .. import service
from ...spider.service import save_cookies, save_time


async def handle(
        jc: int,
        results: list,
        index: int,
        jxlmc: str,
        day: str,
):
    item: dict = results[index]
    jsmph, jasdm = item['jsmph'], item['JASDM']
    item_id, zylxdm = item['id'], item['zylxdm']
    jc_ks, jc_js = item['jc_ks'], item['jc_js']
    obj = {
        'jc': jc,
        'item': item,
        'index': index,
        'results': results,
    }

    if await check_with_ehall(jasdm=jasdm, day=day, jc=str(jc), zylxdm=zylxdm):
        if zylxdm == '00':
            week_count, total_count = await auto_correct(jxl=jxlmc, jsmph=jsmph, jasdm=jasdm, day=day, jc=str(jc))
            app['mail'](
                subject="【南师教室】用户反馈："
                        f"{jxlmc} "
                        f"{jsmph}教室 "
                        f"{jc_ks}-{jc_js}节有误 "
                        f"（当前为第{jc}节）",
                content="验证一站式平台：数据一致\n"
                        f"上报计数：{total_count}\n"
                        f"本周计数：{week_count}\n"
                        f"操作方案：{'自动纠错' if total_count != week_count else None}\n"
                        f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
            )

        else:
            app['mail'](
                subject="【南师教室】用户反馈："
                        f"{jxlmc} "
                        f"{jsmph}教室 "
                        f"{jc_ks}-{jc_js}节有误 "
                        f"（当前为第{jc}节）",
                content=f"验证一站式平台：数据一致（非空教室）\n"
                        f"操作方案：None"
                        f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
            )

    else:
        import manage
        spider = Process(target=manage.main, kwargs=dict(module='spider'))
        spider.start()
        spider.join()
        await service.reset()
        app['mail'](
            subject="【南师教室】用户反馈："
                    f"{jxlmc} "
                    f"{jsmph}教室 "
                    f"{jc_ks}-{jc_js}节有误 "
                    f"（当前为第{jc}节）",
            content=f"验证一站式平台：数据不一致\n"
                    f"操作方案：更新数据库\n"
                    f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
        )


async def check_with_ehall(jasdm: str, day: str, jc: str, zylxdm: str):
    async with aioredis.lock(app['redis'], 'spider'):
        await save_cookies(), await save_time()
        async with aioredis.start(app['redis']) as redis:
            cookies = json.loads(await redis.hget("spider", "cookies"))
            time_info = json.loads(await redis.hget("spider", "time_info"))
            await redis.delete("spider")
    async with aiohttp.request(
            method="POST",
            url="http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do",
            cookies=cookies,
            data=dict(
                XNXQDM=time_info['XNXQDM'][0],
                ZC=time_info['ZC'],
                JASDM=jasdm,
            )
    ) as resp:
        res = await resp.json(content_type=None)
    day_mapper = {
        'Mon.': 0,
        'Tue.': 1,
        'Wed.': 2,
        'Thu.': 3,
        'Fri.': 4,
        'Sat.': 5,
        'Sun.': 6,
    }
    kcb = json.loads(res['datas']['cxyzjskjyqk']['rows'][0]['BY1'])[day_mapper[day]]
    for row in kcb:
        if jc in row['JC'].split(',') and row['ZYLXDM'] in (zylxdm, ''):
            return True  # 数据一致，待纠错
    return False  # 数据不一致，待更新


async def auto_correct(jxl: str, jsmph: str, jasdm: str, day: str, jc: str):
    mysql: aiomysql.MySQL = app['mysql']
    await mysql.execute(
        "INSERT INTO `feedback_metadata` (jc, JASDM) VALUES (%(jc)s, %(jasdm)s)",
        dict(
            jc=jc,
            jasdm=jasdm
        )
    )

    day_mapper = {
        'Sun.': 1,
        'Mon.': 2,
        'Tue.': 3,
        'Wed.': 4,
        'Thu.': 5,
        'Fri.': 6,
        'Sat.': 7,
    }
    statistic = await mysql.fetchall(
        "SELECT DATE_FORMAT(`feedback_metadata`.`time`, '%%Y-%%m-%%d') `date`, COUNT(*) `count` "
        "FROM `feedback_metadata` "
        "WHERE `JASDM`=%(jasdm)s "
        "AND DAYOFWEEK(time)=%(day_of_week)s "
        "AND `jc`=%(jc)s "
        "GROUP BY `date` "
        "ORDER BY `date`",
        dict(
            jasdm=jasdm,
            day_of_week=day_mapper[day],
            jc=jc
        )
    )

    week_count = statistic[-1]['count']
    total_count = sum([row['count'] for row in statistic])
    if week_count != total_count:
        await mysql.execute(
            "INSERT INTO `correction` ("
            "day, JXLMC, jsmph, JASDM, jc_ks, jc_js, jyytms, kcm"
            ") VALUES ("
            "%(day)s, %(jxlmc)s, %(jsmph)s, %(jasdm)s,  %(jc)s, %(jc)s, '占用','####占用'"
            ")",
            dict(
                day=day,
                jxlmc=jxl,
                jsmph=jsmph,
                jasdm=jasdm,
                jc=jc
            )
        )
    return week_count, total_count
