#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _db_manager
""""""
import json

from pymysql.err import OperationalError

from ._mysql import MySQL

__database = MySQL(**json.load(open('conf/database.json')))
__weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

try:
    __database.update('')
except OperationalError:
    print('数据库连接失败')
    print('Exit with code', 4)
    exit(4)


def truncate() -> int:
    """
    清空数据库
    :return:updated count
    """
    return __database.update_batch(*[
        ('truncate table `%s`' % weekday,) for weekday in __weekdays
    ])


def save(weekday, args_list) -> int:
    """
    添加进数据库
    :param weekday:星期几
    :param args_list:参数列表
    :return:updated count
    """
    return __database.update_batch(*[(
        "INSERT INTO `%s`"
        "(`jsmph`, `jxl`,`jasdm`,`capacity`,`zylxdm`,`jc_ks`,`jc_js`,`jyytms`,`kcm`) VALUES "
        "(%%(jsmph)s,%%(jxl)s,%%(jasdm)s,%%(capacity)s,%%(zylxdm)s,%%(jc_ks)s,%%(jc_js)s,%%(jyytms)s,%%(kcm)s)"
        % __weekdays[weekday],
        args
    ) for args in args_list
    ])
