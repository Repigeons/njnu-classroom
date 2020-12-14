#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/14 0014
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  redis_manager.py
""""""
from redis import StrictRedis, ConnectionPool

__pool = ConnectionPool(decode_responses=True)


def get_redis() -> StrictRedis:
    return StrictRedis(connection_pool=__pool)
