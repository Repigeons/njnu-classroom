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
from handler.Classroom import Classroom

buildings: Dict[str, List[Classroom]] = {}


def reset():
    buildings.clear()
    for d, day in enumerate(["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]):
        result = utils.database.fetchall(f"SELECT * FROM `{day}`")
        for item in result:
            classroom = Classroom.load(item)
            classroom.day = d
            if classroom.jasdm not in buildings.keys():
                buildings[classroom.jasdm] = []
            buildings[classroom.jasdm].append(classroom)


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
    classrooms = [classroom.dict for classroom in buildings[args['jasdm']]]
    for i in range(len(classrooms)):
        classrooms[i]['id'] = classrooms[i]['rank'] = i + 1
    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': classrooms
    }


reset()
