#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Database.py
""""""
import json

import app
from ._mysql import MySQL

__database_config = json.load(open('conf/database.json'))[app.env]

_database = MySQL(
    host=__database_config['host'],
    port=__database_config['port'],
    user=__database_config['user'],
    passwd=__database_config['password'],
    database=__database_config['database'],
)
