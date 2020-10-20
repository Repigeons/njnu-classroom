#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Index.py
""""""
import datetime

import app
import utils
from handler.Classroom import Classroom

update_time: str
days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
buildings = {
    "信息楼": [[], [], [], [], [], [], []],
    "电教楼": [[], [], [], [], [], [], []],
    "学明楼": [[], [], [], [], [], [], []],
    "学正楼": [[], [], [], [], [], [], []],
    "学海楼": [[], [], [], [], [], [], []],
    "广乐楼": [[], [], [], [], [], [], []],
    "学行楼": [[], [], [], [], [], [], []],
    "学思楼": [[], [], [], [], [], [], []],
}


def reset(name: str = None, day: int = None) -> None:
    global update_time
    if name is None or day is None:
        for building in buildings.keys():
            for day in range(7):
                reset(building, day)
        update_time = now()
        return None
    buildings[name][day].clear()
    result = utils.database.fetchall(
        sql=f"SELECT * FROM `{days[day]}` WHERE `jxl`=%(jxl)s AND `zylxdm` in ('00','10') ORDER BY `zylxdm`",
        args={'jxl': name}
    )
    for item in result:
        buildings[name][day].append(Classroom.load(item))
        buildings[name][day][-1].day = day
    buildings[name][day].sort()


def handler(args: dict) -> dict:
    global update_time
    if app.config['service'] == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    for key in ["jxl", "day", "dqjc"]:
        if key not in args.keys():
            raise KeyError
    if not args['day'].isdigit() or not args['dqjc'].isdigit():
        raise KeyError
    jxl, day, dqjc = args['jxl'], int(args['day']), int(args['dqjc'])
    if update_time != now():
        reset(jxl, day)
    classrooms = []
    for classroom in buildings[jxl][day]:
        if classroom.jc_ks <= dqjc <= classroom.jc_js:
            classrooms.append(classroom.dict)
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


reset()
