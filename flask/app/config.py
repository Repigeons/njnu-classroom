#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  config.py
""""""
import json
import os

env = 'pro' if os.getenv('FLASK_ENV') == 'production' else 'dev'

__config = json.load(open('../conf/config.json'))
