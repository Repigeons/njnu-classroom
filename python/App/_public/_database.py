#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _database.py
""""""
from redis import ConnectionPool

from utils import MariaDB
from utils.aop import bean, configuration


@configuration("database.mysql")
def mysql(): pass


@configuration("database.redis")
def redis(): pass


@bean("mysql")
def mysql_pool():
    return MariaDB(**mysql)


@bean()
def redis_pool():
    return ConnectionPool(**redis)
