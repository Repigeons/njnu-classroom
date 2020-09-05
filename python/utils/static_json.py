#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/9/5 0005
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  static_json.py
""""""
import json


def dump(classrooms: list, filename: str) -> None:
    """
    change list `classrooms` in to dict and save to `filename`
    :return:None
    """

    buildings = []
    details = {}
    for classroom in classrooms:
        if classroom['JXLMC'] not in buildings:
            buildings.append(classroom['JXLMC'])
            details[classroom['JXLMC']] = []
        details[classroom['JXLMC']].append({
            'JXLMC': classroom['JXLMC'],
            'JSMPH': classroom['JASMC'].replace(classroom['JXLMC'], ''),
            'JASDM': classroom['JASDM']
        })
    json.dump(
        {
            'buildings': buildings,
            'details': details
        },
        open(filename, 'w', encoding='utf8'),
        ensure_ascii=False
    )
