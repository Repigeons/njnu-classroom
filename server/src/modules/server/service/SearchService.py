#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from app import app
from ztxlib import aiomysql
from .static import day_mapper


async def handle(args: dict) -> list:
    if 'day' not in args.keys() or args['day'] != "#" and not args['day'].isdigit():
        raise KeyError('day')
    elif 'jc_ks' not in args.keys() or not args['jc_ks'].isdigit():
        raise KeyError('jc_ks')
    elif 'jc_js' not in args.keys() or not args['jc_js'].isdigit():
        raise KeyError('jc_js')
    elif 'jxl' not in args.keys():
        raise KeyError('jxl')
    elif 'zylxdm' not in args.keys():
        raise KeyError('zylxdm')
    elif 'kcm' not in args.keys():
        raise KeyError('kcm')

    args['keyword'] = f"%{args['kcm']}%"

    mysql: aiomysql.MySQL = app['mysql']
    rows = await mysql.fetchall(
        "SELECT * FROM `pro` WHERE (%(_day)s) AND (%(_jc)s) AND (%(_jxl)s) AND (%(_zylxdm)s) AND (%(_keyword)s)"
        % dict(
            _day=True if args['day'] == "#" else f"`day`='{day_mapper[int(args['day'])]}'",
            _jc="`jc_ks`>=%(jc_ks)s AND `jc_js`<=%(jc_js)s",
            _jxl=True if args['jxl'] == "#" else "`JXLMC`=%(jxl)s",
            _zylxdm=True if args['zylxdm'] == "#" else "`zylxdm`=%(zylxdm)s",
            _keyword="`jyytms` LIKE %(keyword)s OR `kcm` LIKE %(keyword)s",
        ),
        args
    )
    return [
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
    ]
