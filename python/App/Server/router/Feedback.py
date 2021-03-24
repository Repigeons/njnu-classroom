#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
import json
import logging
from multiprocessing import Process

import requests
from flask import current_app as app, request, jsonify
from redis import StrictRedis
from redis_lock import Lock

import App.Server._ApplicationContext as Context
from App.Server._ApplicationContext import send_email
from App.Spider.app import save_cookies, save_time


@app.route('/feedback', methods=['POST'])
def route_feedback():
    form_data = request.form.to_dict()
    Process(
        target=backend_process,
        kwargs={
            'jc': form_data['jc'],
            'results': json.loads(form_data['results']),
            'index': int(form_data['index']),
            'request_args': form_data,
            'jxlmc': form_data['jxl'],
            'day': int(form_data['day'])
        }
    ).start()
    return jsonify({
        'status': 0,
        'message': "ok",
        'data': "feedback"
    }), 202


def backend_process(
        request_args: dict,
        jc: int,
        results: list,
        index: int,
        jxlmc: str,
        day: int,
):
    try:
        item: dict = results[index]
        jsmph, jasdm = item['jsmph'], item['JASDM']
        item_id, zylxdm = item['id'], item['zylxdm']
        jc_ks, jc_js = item['jc_ks'], item['jc_js']
        obj = {
            'jc': jc,
            'item': item,
            'index': index,
            'results': results,
        }

        if check_with_ehall(jasdm=jasdm, day=day, jc=str(jc), zylxdm=zylxdm):
            if zylxdm == '00':
                week_count, total_count = auto_correct(jxl=jxlmc, jsmph=jsmph, jasdm=jasdm, day=day, jc=str(jc))
                send_email(
                    subject=f"南师教室：用户反馈 "
                            f"{jxlmc} "
                            f"{jsmph}教室 "
                            f"{jc_ks}-{jc_js}节有误 "
                            f"（当前为第{jc}节）",
                    message=f"验证一站式平台：数据一致\n"
                            f"上报计数：{total_count}\n"
                            f"本周计数：{week_count}\n"
                            f"操作方案：{'自动纠错' if total_count != week_count else None}\n"
                            f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
                )

            else:
                send_email(
                    subject=f"南师教室：用户反馈 "
                            f"{jxlmc} "
                            f"{jsmph}教室 "
                            f"{jc_ks}-{jc_js}节有误 "
                            f"（当前为第{jc}节）",
                    message=f"验证一站式平台：数据一致（非空教室）\n"
                            f"操作方案：None"
                            f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
                )

        else:
            import manage
            from .Reset import reset
            manage.main(manage.Namespace(run="Spider"))
            reset()

            send_email(
                subject=f"南师教室：用户反馈 "
                        f"{jxlmc} "
                        f"{jsmph}教室 "
                        f"{jc_ks}-{jc_js}节有误 "
                        f"（当前为第{jc}节）",
                message=f"验证一站式平台：数据不一致\n"
                        f"操作方案：更新数据库\n"
                        f"反馈数据详情：{json.dumps(obj, ensure_ascii=False, indent=2)}\n"
            )

    except Exception as e:
        logging.warning(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{request.url}\n"
                    f"{request_args}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )


def check_with_ehall(jasdm: str, day: int, jc: str, zylxdm: str):
    redis = StrictRedis(connection_pool=Context.redis_pool)
    lock = Lock(redis, "Spider")
    if lock.acquire():
        try:
            save_cookies(), save_time()
            cookies = json.loads(redis.hget("Spider", "cookies"))
            time_info = json.loads(redis.hget("Spider", "time_info"))
            redis.delete("Spider")
            res = requests.post(
                url="http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do",
                cookies=cookies,
                data={
                    'XNXQDM': time_info['XNXQDM'][0],
                    'ZC': time_info['ZC'],
                    'JASDM': jasdm
                }
            ).json()
            kcb = json.loads(res['datas']['cxyzjskjyqk']['rows'][0]['BY1'])[(day + 6) % 7]
            for row in kcb:
                if jc in row['JC'].split(',') and row['ZYLXDM'] in (zylxdm, ''):
                    return True  # 数据一致，待纠错
            return False  # 数据不一致，待更新

        finally:
            lock.release()


def auto_correct(jxl: str, jsmph: str, jasdm: str, day: int, jc: str):
    connection, cursor = Context.mysql.get_connection_cursor()
    try:
        cursor.execute(
            "INSERT INTO `feedback_metadata` (jc, JASDM) VALUES (%(jc)s, %(jasdm)s)",
            {
                'jasdm': jasdm,
                'jc': jc,
                'day': day
            }
        )
    finally:
        cursor.close(), connection.close()
    connection, cursor = Context.mysql.get_connection_cursor()
    try:
        cursor.execute(
            "SELECT DATE_FORMAT(`feedback_metadata`.`time`, '%%Y-%%m-%%d') `date`, COUNT(*) `count` "
            "FROM `feedback_metadata` "
            "WHERE `JASDM`=%(jasdm)s "
            "AND DAYOFWEEK(`feedback_metadata`.`time`)-1=%(day)s "
            "AND `jc`=%(jc)s "
            "GROUP BY `date` "
            "ORDER BY `date`",
            {
                'jasdm': jasdm,
                'jc': jc,
                'day': day
            }
        )
        statistic = cursor.fetchall()
    finally:
        cursor.close(), connection.close()
    week_count = statistic[-1].count
    total_count = sum([row.count for row in statistic])
    if week_count != total_count:
        try:
            connection, cursor = Context.mysql.get_connection_cursor()
            cursor.execute(
                "INSERT INTO `correction` ("
                "day, JXLMC, jsmph, JASDM, jc_ks, jc_js, jyytms, kcm"
                ") VALUES ("
                "%(day)s, %(JXLMC)s, %(jsmph)s, %(JASDM)s,  %(jc)s, %(jc)s, '占用','####占用'"
                ")",
                {
                    'day': ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day],
                    'JXLMC': jxl,
                    'jsmph': jsmph,
                    'JASDM': jasdm,
                    'jc': jc
                }
            )
        finally:
            cursor.close(), connection.close()
    return week_count, total_count
