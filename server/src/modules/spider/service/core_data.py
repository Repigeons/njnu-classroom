#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import datetime
import json

import aiohttp

from app import app
from ztxlib import aiomysql


async def get_data(cookies: dict, time_info: dict, classroom: dict) -> list[dict]:
    """
    获取具体课程信息
    :param cookies
    :param time_info
    :param classroom
    """
    today = datetime.datetime.now().weekday()
    this_week = time_info['ZC']
    next_week = time_info['ZC'] + 1 if time_info['ZC'] < time_info['ZJXZC'] else time_info['ZJXZC']
    term_code = time_info['XNXQDM'][0]
    async with aiohttp.request(
            method="POST",
            url="http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do",
            cookies=cookies,
            data=dict(
                XNXQDM=term_code,
                ZC=this_week,
                JASDM=classroom['JASDM'],
            )
    ) as resp:
        res = await resp.json()
    try:
        kcb = json.loads(res['datas']['cxyzjskjyqk']['rows'][0]['BY1'])
    except KeyError:
        return []

    if next_week != this_week:
        async with aiohttp.request(
                method="POST",
                url="http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do",
                cookies=cookies,
                data=dict(
                    XNXQDM=term_code,
                    ZC=next_week,
                    JASDM=classroom['JASDM'],
                )
        ) as resp:
            res = await resp.json()
        try:
            kcb_next = json.loads(res['datas']['cxyzjskjyqk']['rows'][0]['BY1'])
            for day in range(today):
                kcb[day] = kcb_next[day]
        except KeyError:
            pass
    result = []
    for day in range(7):
        for row in kcb[day]:
            jc = row['JC'].split(',')
            item = dict(
                day=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'][day],
                zylxdm='00' if row['ZYLXDM'] == '' else row['ZYLXDM'],
                jc_ks=int(jc[0]),
                jc_js=int(jc[-1]),
                jyytms=row['JYYTMS'] if 'JYYTMS' in row else '',
                kcm=row['KCM'] if 'KCM' in row else '',
            )
            for key in classroom:
                item[key] = classroom[key]
            result.append(item)
            # print([
            #     item['day'], item['jc_ks'], item['jc_js'],
            #     classroom['JXLMC'], classroom['jsmph'],
            #     item['zylxdm'], item['jyytms'], item['kcm']
            # ])
    return result


async def save_data(data: list[dict]):
    mysql: aiomysql.MySQL = app['mysql']
    await mysql.execute(
        "INSERT INTO `KCB`("
        "`JXLMC`, `jsmph`, `JASDM`, `SKZWS`, `zylxdm`, "
        "`jc_ks`, `jc_js`, `jyytms`, `kcm`,`day`, `SFYXZX`"
        ") VALUES ("
        "%(JXLMC)s, %(jsmph)s, %(JASDM)s, %(SKZWS)s, %(zylxdm)s,"
        "%(jc_ks)s, %(jc_js)s, %(jyytms)s, %(kcm)s, %(day)s, %(SFYXZX)s"
        ")",
        *data
    )
