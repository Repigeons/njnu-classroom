#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_time.py
""""""
import json
import time
from json.decoder import JSONDecodeError

import requests

from utils import send_email


def save_time(cookies: dict, file: str) -> None:
    """
    将时间信息保存至文件
    :param cookies: cookies
    :param file: 时间信息文件
    :return: None
    """
    try:
        print('开始尝试查询时间信息...')
        json.dump(
            get_time_info(cookies=cookies),
            open(file, 'w')
        )
        print('时间信息查询完成...')
    except JSONDecodeError:
        send_email(subject="南师教室：错误报告", message=f"JSONDecodeError\ncookies无效\nat line 68")
        print('cookies无效')
        print('Exit with code', 2)
        exit(2)
    except KeyError:
        send_email(subject="南师教室：错误报告", message=f"KeyError\n获取时间信息失败\nat line 73")
        print('获取时间信息失败')
        print('Exit with code', 3)
        exit(3)


def get_time_info(cookies: dict) -> dict:
    """
    获取时间相关信息
    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :return:dict{学年学期代码, 学年代码, 学期代码, 周次, 总周次, 总教学周次}
    """
    result = {}

    # 查询当前学年学期
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do',
        cookies=cookies
    ).json()
    result['XNXQDM'] = res['datas']['cxdqxnxq']['rows'][0]['DM'],
    result['XNDM'] = res['datas']['cxdqxnxq']['rows'][0]['XNDM'],
    result['XQDM'] = res['datas']['cxdqxnxq']['rows'][0]['XQDM']

    # 查询当前周次和总周次
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do',
        cookies=cookies,
        data={
            'XN': result['XNDM'],
            'XQ': result['XQDM'],
            'RQ': time.strftime('%Y-%m-%d', time.localtime())
        }
    ).json()
    result['ZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZC']
    result['ZZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZZC']

    # 查询总教学周次
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do',
        cookies=cookies,
        data={
            'XN': result['XNDM'],
            'XQ': result['XQDM'],
            'SFSY': 1
        }
    ).json()
    result['ZJXZC'] = res['datas']['cxxljc']['rows'][0]['ZJXZC']

    return result
