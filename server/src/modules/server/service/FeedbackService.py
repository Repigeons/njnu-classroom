#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
from email.mime.text import MIMEText
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
        day: int,
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

    if check_with_ehall(jasdm=jasdm, day=day, jc=str(jc), zylxdm=zylxdm):
        if zylxdm == '00':
            week_count, total_count = auto_correct(jxl=jxlmc, jsmph=jsmph, jasdm=jasdm, day=day, jc=str(jc))
            async with app['smtp'] as smtp:
                await smtp.send(
                    **app['mail'],
                    subject="【南师教室】用户反馈："
                            f"{jxlmc} "
                            f"{jsmph}教室 "
                            f"{jc_ks}-{jc_js}节有误 "
                            f"（当前为第{jc}节）",
                    mime_parts=[MIMEText(
                        "验证一站式平台：数据一致\n"
                        f"上报计数：{total_count}\n"
                        f"本周计数：{week_count}\n"
                        f"操作方案：{'自动纠错' if total_count != week_count else None}\n"
                        f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
                    )])

        else:
            async with app['smtp'] as smtp:
                await smtp.send(
                    **app['mail'],
                    subject="【南师教室】用户反馈："
                            f"{jxlmc} "
                            f"{jsmph}教室 "
                            f"{jc_ks}-{jc_js}节有误 "
                            f"（当前为第{jc}节）",
                    mime_parts=[MIMEText(
                        f"验证一站式平台：数据一致（非空教室）\n"
                        f"操作方案：None"
                        f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
                    )])

    else:
        import manage
        spider = Process(target=manage.main, kwargs=dict(module='spider'))
        spider.start()
        spider.join()
        await service.reset()
        async with app['smtp'] as smtp:
            await smtp.send(
                **app['mail'],
                subject="【南师教室】用户反馈："
                        f"{jxlmc} "
                        f"{jsmph}教室 "
                        f"{jc_ks}-{jc_js}节有误 "
                        f"（当前为第{jc}节）",
                mime_parts=[MIMEText(
                    f"验证一站式平台：数据不一致\n"
                    f"操作方案：更新数据库\n"
                    f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
                )])


async def check_with_ehall(jasdm: str, day: int, jc: str, zylxdm: str):
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
        res = await resp.json()
    kcb = json.loads(res['datas']['cxyzjskjyqk']['rows'][0]['BY1'])[(day + 6) % 7]
    for row in kcb:
        if jc in row['JC'].split(',') and row['ZYLXDM'] in (zylxdm, ''):
            return True  # 数据一致，待纠错
    return False  # 数据不一致，待更新


async def auto_correct(jxl: str, jsmph: str, jasdm: str, day: int, jc: str):
    mysql: aiomysql.MySQL = app['mysql']
    await mysql.execute(
        "INSERT INTO `feedback_metadata` (jc, JASDM) VALUES (%(jc)s, %(jasdm)s)",
        dict(
            jc=jc,
            jasdm=jasdm
        )
    )

    statistic = await mysql.fetchall(
        "SELECT DATE_FORMAT(`feedback_metadata`.`time`, '%%Y-%%m-%%d') `date`, COUNT(*) `count` "
        "FROM `feedback_metadata` "
        "WHERE `JASDM`=%(jasdm)s "
        "AND DAYOFWEEK(`feedback_metadata`.`time`)-1=%(day)s "
        "AND `jc`=%(jc)s "
        "GROUP BY `date` "
        "ORDER BY `date`",
        dict(
            jasdm=jasdm,
            day=day,
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
                day=['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day],
                jxlmc=jxl,
                jsmph=jsmph,
                jasdm=jasdm,
                jc=jc
            )
        )
    return week_count, total_count