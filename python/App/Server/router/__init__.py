#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __init__.py
""""""
from .Empty import reset as __reset_empty
from .Overview import reset as __reset_overview

from . import Empty, Overview, SearchMore, Feedback


def reset():
    from App.public import get_redis
    redis = get_redis()
    redis.delete("Empty")
    redis.delete("Overview")
    __reset_empty()
    __reset_overview()
