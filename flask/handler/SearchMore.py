#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  SearchMore.py
""""""
import app
import utils
from handler.Classroom import Classroom


def handler(args: dict) -> dict:
    if app.config['service'] == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    for key in ["day", "jc_ks", "jc_js", "jxl", "zylxdm", "kcm"]:
        if key not in args.keys():
            raise KeyError
    if args['day'] != "#":
        try:
            int(args['day'])
        except ValueError:
            raise KeyError
    if not args['jc_ks'].isdigit() or not args['jc_js'].isdigit():
        raise KeyError

    kcm = "_" if args['kcm'] == "#" else args['kcm']
    days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    days = days if args['day'] == "#" else [days[int(args['day'])]]
    jc = f"(`jc_ks`>={args['jc_ks']} AND `jc_js`<={args['jc_js']})"
    jxl = "(`jxl` IS NOT NULL)" if args['jxl'] == "#" else f"(`jxl`='{args['jxl']}')"
    zylxdm = "(`zylxdm` IS NOT NULL)" if args['zylxdm'] == "#" else f"(`zylxdm`='{args['zylxdm']}')"

    classrooms = []
    for d, day in enumerate(days):
        result = utils.database.fetchall(
            sql=f"SELECT * FROM `{day}` WHERE {jc} AND {jxl} AND {zylxdm} AND (`jyytms` LIKE %(kcm)s OR `kcm` LIKE %(kcm)s)",
            args={'kcm': f"%{kcm}%"}
        )
        for item in result:
            classroom = Classroom.load(item)
            classroom.day = d if args['day'] == "#" else int(args['day'])
            classrooms.append(classroom.dict)
    for i in range(len(classrooms)):
        classrooms[i]['id'] = classrooms[i]['rank'] = i + 1
    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': classrooms
    }
