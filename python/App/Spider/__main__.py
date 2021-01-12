#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import json
import logging
import os
import time

from redis import StrictRedis
from redis_lock import Lock

import App.Spider._ApplicationContext as Context
import App.Spider.app as app
from App.Spider._ApplicationContext import send_email


def main():
    redis = StrictRedis(connection_pool=Context.redis_pool)
    lock = Lock(redis, "Spider")
    try:
        if lock.acquire(blocking=False):
            try:
                logging.info("开始课程信息收集工作...")
                # 采集基础信息
                prepare()
                # 采集详细信息
                core()
                # 校正并归并数据
                correct_and_merge()
                # 从Redis清除缓存数据
                redis.delete("Spider")
                # 将数据放入生产环境
                app.copy_to_pro() if os.getenv("env") == "pro" else None

                now = time.time() * 1000
                logging.info(
                    "本轮课程信息收集工作成功完成. 共计耗时 %f seconds",
                    (int(now) - int(os.getenv("start_time"))) / 1000
                )
            finally:
                lock.release()
        else:
            logging.warning("Terminated for another process locked [%s]", "Spider")

    except SystemExit or KeyboardInterrupt as e:
        raise e

    except Exception as e:
        logging.error(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", -1)
        exit(-1)


def prepare():
    logging.info("开始采集基础信息...")
    app.save_cookies()
    app.save_time()
    app.save_classrooms()
    time.sleep(5)
    logging.info("基础信息采集完成")


def core():
    logging.info("开始采集详细信息...")
    redis = StrictRedis(connection_pool=Context.redis_pool)
    cookies = json.loads(redis.hget("Spider", "cookies"))
    time_info = json.loads(redis.hget("Spider", "time_info"))
    classrooms = json.loads(redis.hget("Spider", "classrooms"))
    app.truncate_kcb()
    for jxl in classrooms:
        print("开始查询教学楼：", jxl)
        for classroom in classrooms[jxl]:
            print("正在查询教室：", classroom['JXLMC'], classroom['jsmph'])
            result = app.get_detail(cookies=cookies, time_info=time_info, classroom=classroom)
            app.insert_into_kcb(class_list=result)
    time.sleep(5)
    logging.info("详细信息采集完成")


def correct_and_merge():
    # 校正数据
    logging.info("开始校正数据...")
    app.copy_to_dev()
    app.correct()
    time.sleep(5)
    logging.info("校正数据完成")

    # 归并数据
    logging.info("开始归并数据...")
    app.merge()
    time.sleep(5)
    logging.info("归并数据完成")


if __name__ == '__main__':
    main()
