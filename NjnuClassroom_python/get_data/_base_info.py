#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _base_info
""""""
import time

import requests


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


def get_jxl_info(cookies: dict, xn_xq_dm: str) -> list:
    """
    获取教学楼信息

    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :param xn_xq_dm:学年学期代码
    :return:list[dict{教学楼名称, 教学楼代码}]
    """

    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxkxjs1.do',
        cookies=cookies,
        data={
            'XNXQDM': xn_xq_dm,
            'XXQDM': 2,
            'TYPE': 2,
            '*order': '+JASDM'
        }
    ).json()
    return [
        {
            'JXLMC': item['JXLMC'],
            'JXLDM': item['JXLDM']
        }
        for item in res['datas']['cxkxjs1']['rows']
    ]


def get_classroom_info(cookies: dict, xn_xq_dm: str, jxl_dm: str) -> list:
    """
    获取教室信息

    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :param xn_xq_dm:学年学期代码
    :param jxl_dm:教学楼代码
    :return:list[dict{教学楼名称, 教室名称, 教室代码, 教室门牌号, 容纳人数}]
    """

    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxkxjs1.do',
        cookies=cookies,
        data={
            'XNXQDM': xn_xq_dm,
            'XXQDM': 2,
            'JXLDM': jxl_dm,
            'TYPE': 3,
            '*order': '+JASDM'
        }
    ).json()
    return [
        {
            'JXLMC': item['JXLMC'],
            'JASMC': item['JASMC'],
            'JASDM': item['JASDM'],
            'JASLXDM': item['JASLXDM'],
            'SKZWS': item['SKZWS']
        }
        for item in res['datas']['cxkxjs1']['rows']
    ]
