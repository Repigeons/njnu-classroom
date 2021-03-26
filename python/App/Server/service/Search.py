#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Search.py
""""""
from App.Server import dao
from utils.aop import autowired, configuration


@autowired()
def day_mapper(): pass


@configuration("application.server.service")
def serve(): pass


def handle_search(args: dict) -> dict:
    if not serve:
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

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
    rows = dao.search(
        _day=True if args['day'] == "#" else f"`day`='{day_mapper[int(args['day'])]}'",
        _jc="`jc_ks`>=%(jc_ks)s AND `jc_js`<=%(jc_js)s",
        _jxl=True if args['jxl'] == "#" else "`JXLMC`=%(jxl)s",
        _zylxdm=True if args['zylxdm'] == "#" else "`zylxdm`=%(zylxdm)s",
        _keyword="`jyytms` LIKE %(keyword)s OR `kcm` LIKE %(keyword)s",
        **args
    )
    result = [
        {
            'JXLMC': row.JXLMC,
            'jsmph': row.jsmph,
            'SKZWS': row.SKZWS,

            'day': day_mapper[row.day],
            'jc_ks': row.jc_ks,
            'jc_js': row.jc_js,

            'zylxdm': row.zylxdm,
            'jyytms': row.jyytms,
            'kcm': row.kcm,
        } for row in rows
    ]

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': result
    }
