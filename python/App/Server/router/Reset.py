#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/15 0015
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Reset.py
""""""
import json
from threading import Lock

from flask import current_app as app, jsonify

from App.Server.router import day_mapper
from App.public import database, get_redis, send_email
from utils import Threading

lock = Lock()


@app.route('/reset', methods=['POST'])
def route():
    try:
        Threading(reset).start()
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': "reset"
        }), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}in app.app: line 35")
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


def reset():
    try:
        lock.acquire()
        redis = get_redis()
        redis.delete("Empty")
        redis.delete("Overview")
        reset_empty()
        reset_overview()
    finally:
        lock.release()


def reset_empty():
    redis = get_redis()
    for jxl in database.fetchall("SELECT DISTINCT `JXLDM_DISPLAY` FROM `JAS` WHERE `_SFYXZX`"):
        jxlmc = jxl[0]
        for day in range(7):
            redis.hset(
                name="Empty",
                key=f"{jxlmc}_{day}",
                value=json.dumps([
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
                    } for item in database.fetchall(
                        sql=f"SELECT * FROM `pro` "
                            f"WHERE `JXLMC`=%(JXLMC)s AND `day`=%(day)s AND `zylxdm` in ('00', '10') AND `_SFYXZX`"
                            f"ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`",
                        args={'JXLMC': jxlmc, 'day': day_mapper[day]}
                    )
                ])
            )


def reset_overview():
    redis = get_redis()
    for jasdm in database.fetchall("SELECT DISTINCT `JASDM` FROM `JAS`"):
        redis.hset(
            name="Overview",
            key=jasdm[0],
            value=json.dumps([
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
                database.fetchall("SELECT * FROM `pro` WHERE `JASDM`=%(jasdm)s", {'jasdm': jasdm[0]})
            ])
        )
