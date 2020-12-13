#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/13 0013
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
from flask import current_app as app, request, jsonify

with open("resource/shuttleTimetable.csv", encoding='utf8') as f:
    stream = f.read().split('\n\n')
    f.close()
stations = {sp[0]: [float(sp[1]), float(sp[2])] for sp in [station.split('|') for station in stream[0].split(',')]}
routes1 = [
    line.split(',')
    for line in stream[1].split()
]
routes2 = [
    line.split(',')
    for line in stream[2].split()
]


@app.route('/shuttle.json', methods=['GET'])
def xnbc():
    return jsonify({'stations': stations, 'routes1': routes1, 'routes2': routes2})
