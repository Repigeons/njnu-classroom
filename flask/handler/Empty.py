#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Empty.py
""""""
import datetime

import app
import utils

days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
day_mapper = {"sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6}

update_time: str
buildings = {}


def reset_buildings():
    buildings.clear()
    jxl_list = utils.database.fetchall("SELECT DISTINCT `JXLDM_DISPLAY` FROM `JAS` WHERE `_SFYXZX`")
    for jxl in jxl_list:
        buildings[jxl['JXLDM_DISPLAY']] = [[] for _ in range(7)]


def reset_all():
    reset_buildings()

    global update_time
    for building in buildings.keys():
        for day in range(7):
            reset(building, day)
    update_time = now()


def reset(jxl: str, day: int) -> None:
    buildings[jxl][day] = [
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
        } for item in utils.database.fetchall(
            sql=f"SELECT * FROM `pro` WHERE `JXLMC`=%(JXLMC)s AND `day`=%(day)s AND `zylxdm` in ('00', '10') AND `_SFYXZX`"
                f"ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`",
            args={'JXLMC': jxl, 'day': days[day]}
        )
    ]


def handler(args: dict) -> dict:
    global update_time
    if app.config['service'] == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    if 'jxl' not in args.keys() or args['jxl'] not in buildings.keys():
        raise KeyError('jxl')
    elif 'day' not in args.keys() or not args['day'].isdigit():
        raise KeyError('day')
    elif 'dqjc' not in args.keys() or not args['dqjc'].isdigit():
        raise KeyError('dqjc')

    jxl, day, dqjc = args['jxl'], int(args['day']), int(args['dqjc'])
    if update_time != now():
        reset(jxl, day)

    classrooms = []
    for classroom in buildings[jxl][day]:
        if classroom['jc_ks'] <= dqjc <= classroom['jc_js']:
            classrooms.append(classroom)
    for i in range(len(classrooms)):
        classrooms[i]['id'] = classrooms[i]['rank'] = i + 1
    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': classrooms
    }


def now() -> str:
    return datetime.datetime.now().strftime('%x')


reset_all()
