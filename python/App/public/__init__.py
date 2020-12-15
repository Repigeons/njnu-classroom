#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __init__.py
""""""
# public Object
from .database_manager import _database as database

# public method
from .mail_manager import send_email
from .redis_manager import get_redis
