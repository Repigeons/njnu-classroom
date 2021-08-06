#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aioredis import RedisError


class RedisTimeoutError(RedisError, TimeoutError):
    pass


class WaitingTimeoutError(RedisTimeoutError):
    pass


class RunningTimeoutError(RedisTimeoutError):
    pass


class UnlockError(RedisError):
    pass
