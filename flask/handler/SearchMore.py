#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  SearchMore.py
""""""
import app
import utils

days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
day_mapper = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6}


def handler(args: dict) -> dict:
    if app.config['service'] == 'off':
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

    jc = "`jc_ks`>=%(jc_ks)s AND `jc_js`<=%(jc_js)s"
    day = True if args['day'] == "#" else f"`day`={days[int(args['day'])]}"
    jxl = True if args['jxl'] == "#" else "`jxl`=%(jxl)s"
    zylxdm = True if args['zylxdm'] == "#" else "`zylxdm`=%(zylxdm)s"
    keyword = "`jyytms` LIKE %(keyword)s OR `kcm` LIKE %(keyword)s"
    args['keyword'] = f"%{args['kcm']}%"

    result = [
        {
            'jasdm': item['JASDM'],
            'JASDM': item['JASDM'],

            'jxl': item['JXLMC'],
            'JXLMC': item['JXLMC'],

            'jsmph': item['jsmph'],

            'capacity': item['SKZWS'],
            'SKZWS': item['SKZWS'],

            'day': day_mapper[item['day']],
            'jc_ks': item['jc_ks'],
            'jc_js': item['jc_js'],

            'zylxdm': item['zylxdm'],
            'jyytms': item['jyytms'],
            'kcm': item['kcm'],
        } for item in
        utils.database.fetchall(
            sql=f"SELECT * FROM `pro` WHERE ({day}) AND ({jc}) AND ({jxl}) AND ({zylxdm}) AND ({keyword})",
            args=args
        )
    ]

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': result
    }
