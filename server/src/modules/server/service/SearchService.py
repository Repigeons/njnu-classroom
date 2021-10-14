#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import os

from app import app
from exceptions import RequestParameterError
from ztxlib import aiomysql


async def handle(day: str,
                 jc_ks: int,
                 jc_js: int,
                 jxl: str,
                 zylxdm: str,
                 keyword: str) -> list:
    if not (1 <= jc_ks <= jc_js <= 12):
        raise RequestParameterError('jc_ks,jc_js')
    if day != '#':
        if day not in ['Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.']:
            raise RequestParameterError('day')
    keyword = '%' if keyword == '#' else f'%{keyword}%'

    env = os.getenv('env', 'dev')
    env = 'pro' if env == 'pro' else 'dev'

    mysql: aiomysql.MySQL = app['mysql']
    rows = await mysql.fetchall(
        f"SELECT * FROM `{env}` WHERE (%(_day)s) AND (%(_jc)s) AND (%(_jxl)s) AND (%(_zylxdm)s) AND (%(_keyword)s)"
        % dict(
            _day=True if day == '#' else f"`day`=%(day)s",
            _jc="`jc_ks`>=%(jc_ks)s AND `jc_js`<=%(jc_js)s",
            _jxl=True if jxl == '#' else "`JXLMC`=%(jxl)s",
            _zylxdm=True if zylxdm == '#' else "`zylxdm`=%(zylxdm)s",
            _keyword="`jyytms` LIKE %(keyword)s OR `kcm` LIKE %(keyword)s",
        ),
        dict(
            day=day,
            jc_ks=jc_ks,
            jc_js=jc_js,
            jxl=jxl,
            zylxdm=zylxdm,
            keyword=keyword,
        )
    )
    return [
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
    ]
