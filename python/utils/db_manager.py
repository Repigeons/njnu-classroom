#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _db_manager
""""""
import json
from sys import exit

from pymysql import DatabaseError

from ._mysql import MySQL

__db_config = json.load(open('conf/database.json'))
__database_dev = MySQL(**__db_config['dev'])
__database_pro = MySQL(**__db_config['pro'])
__weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

if not __database_dev.test_connection():
    print('数据库连接失败')
    print('Exit with code', 4)
    exit(4)


def truncate() -> int:
    """
    清空数据库
    :return:updated count
    """
    return __database_dev.update_batch(*[
        ('truncate table `%s`' % weekday,) for weekday in __weekdays
    ])


def insert(weekday, args_list) -> int:
    """
    添加进数据库
    :param weekday:星期几
    :param args_list:参数列表
    :return:updated count
    """
    return __database_dev.update_batch(*[(
        "INSERT INTO `%s`"
        "(`jsmph`, `jxl`,`jasdm`,`capacity`,`zylxdm`,`jc_ks`,`jc_js`,`jyytms`,`kcm`) VALUES "
        "(%%(jsmph)s,%%(jxl)s,%%(jasdm)s,%%(capacity)s,%%(zylxdm)s,%%(jc_ks)s,%%(jc_js)s,%%(jyytms)s,%%(kcm)s)"
        % __weekdays[weekday],
        args
    ) for args in args_list
    ])


def save_to_pro():
    for day in __weekdays:
        while True:
            try:
                __database_pro.update(f"truncate table `kcb`.`{day}`")
                __database_pro.update(f"insert into `kcb`.`{day}` select * from `kcb_dev`.`{day}`")
                break
            except DatabaseError:
                continue
