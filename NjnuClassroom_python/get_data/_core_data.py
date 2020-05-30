#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _core_data
""""""
import datetime
import json
import time

import requests


def get_class_info(cookies: dict, xn_xq_dm: str, jas_dm: str, zc: int) -> list:
    """
    获取指定周次的数据

    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :param xn_xq_dm:学年学期代码
    :param jas_dm:教室代码
    :param zc:周次
    :return:list[dict{}]
    """
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxyzjskjyqk.do',
        cookies=cookies,
        data={
            'XNXQDM': xn_xq_dm,
            'ZC': zc,
            'JASDM': jas_dm
        }
    ).json()
    res = json.loads(res['datas']['cxyzjskjyqk']['rows'][0]['BY1'])
    for i in range(7):
        for item in res[i]:
            _analyse_jc(item)
            item['JYYTMS'] = item['JYYTMS'] if 'JYYTMS' in item else ''
            item['KCM'] = item['KCM'] if 'KCM' in item else ''
        _combine_empty(res[i])
    return res


def _analyse_jc(item: dict) -> None:
    """
    修改节次格式
    :param item:需要修改的项目
    :return:None
    """
    jc = item['JC'].split(',')
    item['JC'] = [
        int(jc[0]),
        int(jc[-1])
    ]


def _combine_empty(items: list) -> None:
    """
    合并空项目

    :param items:待合并的项目列表
    :return:None
    """
    i = 0
    while i < len(items) - 1:
        if not items[i]['ZYLXDM'] and not items[i + 1]['ZYLXDM']:
            items[i]['JC'][1] = items[i + 1]['JC'][1]
            items.pop(i + 1)
        else:
            i += 1
    for item in items:
        item['ZYLXDM'] = '00'


def get_class_weekly(cookies: dict, xn_xq_dm: str, jas_dm: str, zc: int, zzc: int) -> list:
    """
    获取当日起一周内的数据

    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :param xn_xq_dm:学年学期代码
    :param jas_dm:教室代码
    :param zc:当前周次
    :param zzc:总周次
    :return:
    """
    time.sleep(.2)
    result = []
    this_week = get_class_info(cookies, xn_xq_dm, jas_dm, zc)

    if zc == zzc:
        return this_week
    else:
        next_week = get_class_info(cookies, xn_xq_dm, jas_dm, zc + 1)
        today = datetime.datetime.now().weekday()
        for weekday in range(today):
            result.append(next_week[weekday])
        for weekday in range(today, 7):
            result.append(this_week[weekday])
        return result
