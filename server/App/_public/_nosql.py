#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/21
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _nosql.py
""""""
from redis import ConnectionPool
from ztxlib.rpspring import Bean
from ztxlib.rpspring import Value


@Value("database.redis")
def redis_config() -> dict: pass


@Bean
def redis_pool():
    return ConnectionPool(**redis_config)
