#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Main.py
""""""
import datetime
import json
import os
import shutil
import time

import utils
import app

temp_dir = '~tmp'


def prepare():
    app.save_cookies(file=f"{temp_dir}/cookies.json")
    cookies = json.load(open(f"{temp_dir}/cookies.json"))
    app.save_time(cookies=cookies, file=f"{temp_dir}/time_info.json")
    app.save_classrooms(f"{temp_dir}/classrooms.json")


def main():
    cookies = json.load(open(f"{temp_dir}/cookies.json"))
    time_info = json.load(open(f"{temp_dir}/time_info.json"))
    classrooms = json.load(open(f"{temp_dir}/classrooms.json"))

    utils.truncate_kcb()
    for jxl in classrooms:
        print('开始查询教学楼：', jxl)
        for classroom in classrooms[jxl]:
            print('正在查询教室:', classroom['JXLMC'], classroom['jsmph'])
            result = app.get_detail(cookies=cookies, time_info=time_info, classroom=classroom)
            utils.insert_into_kcb(class_list=result)


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-env', default='dev', type=str, help="developing environment or production environment")
    parser.add_argument('-phantomjs', default='phantomjs', type=str, help="phantomjs path")
    args = parser.parse_args()

    app.set_phantomjs(args.phantomjs)

    try:
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        print(datetime.datetime.now().strftime('[%Y-%m-%d %X]'), '开始课程信息收集工作。')

        prepare()
        print('基础信息采集完成...')

        print('即将开始采集详细信息...')
        time.sleep(5)
        main()
        print('详细信息采集完成...')

        print('即将开始校正数据...')
        time.sleep(5)
        utils.copy_to_dev()
        utils.correct()
        print('校正数据完成...')

        print('即将开始归并数据...')
        time.sleep(5)
        utils.merge(temp_dir=temp_dir)
        print('数据归并完成...')

        if args.env == 'pro':
            utils.copy_to_pro()

        print()
        print('--------------------------------------------------')
        print(datetime.datetime.now().strftime('[%Y-%m-%d %X]'), '本轮具体课程信息收集工作成功完成。')
        print()

    except SystemExit or KeyboardInterrupt as exception:
        raise exception
    except Exception as e:
        utils.send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}\nin app._get_cookie at line 75")
        print(type(e), e)
        print('Exit with code', -1)
        exit(-1)
    finally:
        shutil.rmtree(temp_dir)
