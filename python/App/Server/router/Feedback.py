#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
import json
import os
from threading import Lock

import requests
from flask import current_app as app, request, jsonify

from App.Server import router
from App.Spider.app import save_cookies, save_time
from App.public import database, send_email
from utils import Threading

lock = Lock()


@app.route('/feedback', methods=['POST'])
def feedback():
    Threading(backend_process).start(proxy_app=app, request_args=request.form.to_dict())
    return jsonify({
        'status': 0,
        'message': "ok",
        'data': "feedback"
    }), 202


def backend_process(proxy_app, request_args: dict):
    request_args['resultList'] = json.loads(request_args['resultList'])
    request_args['index'] = int(request_args['index'])
    request_args['item'] = request_args['resultList'][request_args['index']]
    request_args['id'] = request_args['item']['id']
    try:
        lock.acquire()
        jc, day = request_args['dqjc'], int(request_args['day'])
        jxl = request_args['item']['JXLMC']
        jsmph = request_args['item']['jsmph']
        jasdm = request_args['item']['JASDM']
        zylxdm = request_args['item']['zylxdm']

        if check_with_ehall(jasdm=jasdm, day=day, jc=jc, zylxdm=zylxdm):

            if zylxdm == '00':
                week_count, total_count = auto_correct(jxl=jxl, jsmph=jsmph, jasdm=jasdm, day=day, jc=jc)
                send_email(
                    subject=f"南师教室：用户反馈 "
                            f"{jxl} "
                            f"{jsmph}教室 "
                            f"{request_args['item']['jc_ks']}-{request_args['item']['jc_js']}节有误 "
                            f"（当前为第{jc}节）",
                    message=f"验证一站式平台：数据一致\n"
                            f"上报计数：{total_count}\n"
                            f"本周计数：{week_count}\n"
                            f"操作方案：{'自动纠错' if total_count != week_count else None}\n"
                            f"反馈数据详情：{json.dumps(request_args, ensure_ascii=False, indent=2)}\n"
                )

            else:
                send_email(
                    subject=f"南师教室：用户反馈 "
                            f"{jxl} "
                            f"{jsmph}教室 "
                            f"{request_args['item']['jc_ks']}-{request_args['item']['jc_js']}节有误 "
                            f"（当前为第{jc}节）",
                    message=f"验证一站式平台：数据一致（非空教室）\n"
                            f"操作方案：None"
                            f"反馈数据详情：{json.dumps(request_args, ensure_ascii=False, indent=2)}\n"
                )

        else:
            from App.Spider.__main__ import main
            main()
            router.reset_empty()
            router.reset_overview()

            send_email(
                subject=f"南师教室：用户反馈 "
                        f"{jxl} "
                        f"{jsmph}教室 "
                        f"{request_args['item']['jc_ks']}-{request_args['item']['jc_js']}节有误 "
                        f"（当前为第{jc}节）",
                message=f"验证一站式平台：数据不一致\n"
                        f"操作方案：更新数据库\n"
                        f"反馈数据详情：{json.dumps(request_args, ensure_ascii=False, indent=2)}\n"
            )

    except Exception as e:
        proxy_app.logger.warning(f"{type(e), e}")

        send_email(
            subject="南师教室：错误报告 in app.router.Feedback",
            message=f"{type(e), e}\n"
                    f"{request.url}\n"
                    f"{request_args}"
        )
    finally:
        lock.release()


def check_with_ehall(jasdm: str, day: int, jc: str, zylxdm: str):
    cookies_file, time_file = "cookies.json", "time.json"
    try:
        save_cookies(file=cookies_file)
        cookies = json.load(open(cookies_file))
    finally:
        os.remove(cookies_file)
    try:
        save_time(cookies=cookies, file=time_file)
        time_info = json.load(open(time_file))
    finally:
        os.remove(time_file)

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


def auto_correct(jxl: str, jsmph: str, jasdm: str, day: int, jc: str):
    database.update(
        sql="INSERT INTO `feedback_metadata` (jc, JASDM) VALUES (%(jc)s, %(jasdm)s)",
        args={
            'jasdm': jasdm,
            'jc': jc,
            'day': day
        }
    )
    statistic = database.fetchall(
        sql="SELECT DATE_FORMAT(`feedback_metadata`.`time`, '%%Y-%%m-%%d') `date`, COUNT(*) `count` "
            "FROM `feedback_metadata` "
            "WHERE `JASDM`=%(jasdm)s "
            "AND DAYOFWEEK(`feedback_metadata`.`time`)-1=%(day)s "
            "AND `jc`=%(jc)s "
            "GROUP BY `date` "
            "ORDER BY `date`",
        args={
            'jasdm': jasdm,
            'jc': jc,
            'day': day
        }
    )
    week_count = statistic[-1]['count']
    total_count = sum([row['count'] for row in statistic])
    if week_count != total_count:
        database.update(
            sql="INSERT INTO `correction` ("
                "day, JXLMC, jsmph, JASDM, jc_ks, jc_js, jyytms, kcm"
                ") VALUES ("
                "%(day)s, %(JXLMC)s, %(jsmph)s, %(JASDM)s,  %(jc)s, %(jc)s, '占用','####占用'"
                ")",
            args={
                'day': ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day],
                'JXLMC': jxl,
                'jsmph': jsmph,
                'JASDM': jasdm,
                'jc': jc
            }
        )
    return week_count, total_count
