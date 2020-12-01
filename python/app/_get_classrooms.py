#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_classrooms.py
""""""
import json

import utils


def save_classrooms(file: str):
    print("开始查询教学楼及教室信息...")
    classrooms = utils.get_classrooms()
    json.dump(classrooms, open(file, 'w', encoding='utf8'))
    print("教学楼及教室信息查询完成...")
