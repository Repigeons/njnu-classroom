#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Overview.py
""""""
from typing import Dict, List

import app
import utils

buildings: Dict[str, List[dict]] = {}


def reset():
    buildings.clear()
    day_mapper = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6}
    for jasdm in utils.database.fetchall("SELECT DISTINCT `JASDM` FROM `JAS`"):
        buildings[jasdm[0]] = [
            {
                'day': day_mapper[item['day']],
                'jasdm': item['JASDM'],
                'jxl': item['JXLMC'],
                'jsmph': item['jsmph'],
                'capacity': item['SKZWS'],
                'zylxdm': item['zylxdm'],
                'jc_ks': item['jc_ks'],
                'jc_js': item['jc_js'],
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

    if 'jasdm' not in args.keys():
        raise KeyError

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': buildings[args['jasdm']]
    }


reset()
