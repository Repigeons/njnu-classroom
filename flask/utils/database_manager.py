#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  database_manager.py
""""""
import json
import os

from ._mysql import MySQL

__env = 'pro' if os.getenv('FLASK_ENV') == 'production' else 'dev'
__database_config = json.load(open('conf/database.json'))

_database = MySQL(**__database_config[__env])
