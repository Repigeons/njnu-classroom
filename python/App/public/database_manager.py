#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  database_manager.py
""""""
import json
import os

from utils import MySQL

__database_config = json.load(open('conf/database.json'))
__env = os.getenv("env")
_database = MySQL(**__database_config[__env])
