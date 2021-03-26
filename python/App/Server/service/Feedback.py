#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
import json
import logging

import requests
from flask import request
from redis import StrictRedis
from redis_lock import Lock

from utils.aop import autowired

from App.Server import dao
from App.Spider.service import save_cookies, save_time


@autowired()
def send_email(subject: str, message: str): _ = subject, message


@autowired()
def redis_pool(): pass


def process(
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
            from . import reset
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
    redis = StrictRedis(connection_pool=redis_pool)
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
    dao.add_feedback(jc=jc, jasdm=jasdm)
    statistic = dao.get_feedback(jasdm=jasdm, day=day, jc=jc)
    week_count = statistic[-1].count
    total_count = sum([row.count for row in statistic])
    if week_count != total_count:
        dao.add_correction(
            day=['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'][day],
            jxlmc=jxl,
            jsmph=jsmph,
            jasdm=jasdm,
            jc=jc
        )
    return week_count, total_count
