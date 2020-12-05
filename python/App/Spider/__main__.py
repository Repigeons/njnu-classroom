#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __main__.py
""""""
import datetime
import json
import os
import shutil
import time

from App.Spider import app, dao
from App.public import database, send_email

env = os.getenv("env")
temp_dir = '~tmp'


def main():
    try:
        None if os.path.exists(temp_dir) else os.mkdir(temp_dir)

        # 开始工作
        print(datetime.datetime.now().strftime('[%Y-%m-%d %X]'), '开始课程信息收集工作。')

        prepare()
        print('基础信息采集完成...')

        print('即将开始采集详细信息...')
        time.sleep(5)
        core()
        print('详细信息采集完成...')

        print('即将开始校正数据...')
        time.sleep(5)
        dao.copy_to_dev()
        dao.correct()
        print('校正数据完成...')

        print('即将开始归并数据...')
        time.sleep(5)
        dao.merge(temp_dir=temp_dir)
        print('数据归并完成...')

        dao.copy_to_pro() if env == 'pro' else None

        print()
        print('--------------------------------------------------')
        print(datetime.datetime.now().strftime('[%Y-%m-%d %X]'), '本轮具体课程信息收集工作成功完成。')
        print()

    except SystemExit or KeyboardInterrupt as e:
        raise e

    except Exception as e:
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}\nin app._get_cookie at line 75")
        print(type(e), e)
        print('Exit with code', -1)
        exit(-1)

    finally:
        shutil.rmtree(temp_dir)


def prepare():
    app.save_cookies(file=f"{temp_dir}/cookies.json")
    cookies = json.load(open(f"{temp_dir}/cookies.json"))
    app.save_time(cookies=cookies, file=f"{temp_dir}/time_info.json")
    app.save_classrooms(f"{temp_dir}/classrooms.json")


def core():
    cookies = json.load(open(f"{temp_dir}/cookies.json"))
    time_info = json.load(open(f"{temp_dir}/time_info.json"))
    classrooms = json.load(open(f"{temp_dir}/classrooms.json"))

    database.update("TRUNCATE TABLE `KCB`")
    for jxl in classrooms:
        print('开始查询教学楼：', jxl)
        for classroom in classrooms[jxl]:
            print('正在查询教室:', classroom['JXLMC'], classroom['jsmph'])
            result = app.get_detail(cookies=cookies, time_info=time_info, classroom=classroom)
            dao.insert_into_kcb(class_list=result)


if __name__ == '__main__':
    main()
