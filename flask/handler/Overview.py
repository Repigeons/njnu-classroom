#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Overview.py
""""""

import app
import utils

day_mapper = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6}

classrooms = {}


def reset():
    classrooms.clear()
    for jasdm in utils.database.fetchall("SELECT DISTINCT `JASDM` FROM `JAS`"):
        classrooms[jasdm[0]] = [
            {
                'jasdm': item['JASDM'],
                'JASDM': item['JASDM'],

                'jxl': item['JXLMC'],
                'JXLMC': item['JXLMC'],

                'classroom': item['jsmph'],
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
            utils.database.fetchall("SELECT * FROM `pro` WHERE `JASDM`=%(jasdm)s", {'jasdm': jasdm[0]})
        ]


def handler(args: dict) -> dict:
    if app.config['service'] == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    if 'jasdm' not in args.keys() or args['jasdm'] not in classrooms.keys():
        raise KeyError('jasdm')

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': classrooms[args['jasdm']]
    }


reset()
