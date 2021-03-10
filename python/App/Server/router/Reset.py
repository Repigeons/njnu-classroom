#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/15 0015
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Reset.py
""""""
import json
import logging
from threading import Thread

from flask import current_app as app, request, jsonify
from redis import StrictRedis
from redis_lock import Lock

import App.Server._ApplicationContext as Context
from App.Server._ApplicationContext import send_email, mysql_reset as mysql


@app.route('/reset', methods=['POST'])
def route_reset():
    try:
        Thread(target=reset).start()
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': "reset"
        }), 202
    except Exception as e:
        logging.warning(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{request.url}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


def reset():
    redis = StrictRedis(connection_pool=Context.redis_pool)
    lock1 = Lock(redis, "Server-Empty")
    lock2 = Lock(redis, "Server-Overview")
    if lock1.acquire(blocking=False):
        try:
            redis.delete("Empty")
            reset_empty()
        finally:
            lock1.release()
    if lock2.acquire(blocking=False):
        try:
            redis.delete("Overview")
            reset_overview()
        finally:
            lock2.release()


def reset_empty():
    redis = StrictRedis(connection_pool=Context.redis_pool)
    connection, cursor = mysql.get_connection_cursor()
    try:
        cursor.execute("SELECT DISTINCT `JXLDM_DISPLAY` FROM `JAS` WHERE `SFYXZX`")
        jxl_list = cursor.fetchall()
    finally:
        cursor.close(), connection.close()
    for jxl in jxl_list:
        jxlmc = jxl.JXLDM_DISPLAY
        for day in range(7):
            connection, cursor = mysql.get_connection_cursor()
            try:
                cursor.execute(
                    "SELECT * FROM `pro` "
                    "WHERE `JXLMC`=%(JXLMC)s AND `day`=%(day)s AND `zylxdm` in ('00', '10') AND `SFYXZX` "
                    "ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`",
                    {'JXLMC': jxlmc, 'day': Context.day_mapper[day]}
                )
                rows = cursor.fetchall()
            finally:
                cursor.close(), connection.close()
            redis.hset(
                name="Empty",
                key=f"{jxlmc}_{day}",
                value=json.dumps([
                    {
                        'JXLMC': jxlmc,  # 教学楼名称  # TODO: DELETE
                        'JASDM': row.jasdm,  # TODO: DELETE

                        'jsmph': row.jsmph,  # 教室门牌号
                        'SKZWS': row.SKZWS,  # 上课座位数
                        'jc_ks': row.jc_ks,  # 开始节次
                        'jc_js': row.jc_js,  # 结束节次
                        'zylxdm': row.zylxdm,  # 资源类型代码
                    } for row in rows
                ])
            )


def reset_overview():
    redis = StrictRedis(connection_pool=Context.redis_pool)
    connection, cursor = mysql.get_connection_cursor()
    try:
        cursor.execute("SELECT DISTINCT `JASDM` FROM `JAS`")
        jas_list = cursor.fetchall()
    finally:
        cursor.close(), connection.close()
    for jas in jas_list:
        connection, cursor = mysql.get_connection_cursor()
        try:
            cursor.execute("SELECT * FROM `pro` WHERE `JASDM`=%(jasdm)s", {'jasdm': jas.JASDM})
            rows = cursor.fetchall()
        finally:
            cursor.close(), connection.close()
        redis.hset(
            name="Overview",
            key=jas.JASDM,
            value=json.dumps([
                {
                    'jxl': row.JXLMC,  # TODO: DELETE
                    'classroom': row.jsmph,  # TODO: DELETE

                    'JXLMC': row.JXLMC,
                    'jsmph': row.jsmph,
                    'SKZWS': row.SKZWS,

                    'day': Context.day_mapper[row.day],
                    'jc_ks': row.jc_ks,
                    'jc_js': row.jc_js,

                    'zylxdm': row.zylxdm,
                    'jyytms': row.jyytms,
                    'kcm': row.kcm,
                } for row in rows
            ])
        )
