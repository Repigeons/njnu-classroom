#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __init__.py
""""""
from .db_manager import truncate, insert, save_to_pro
from .get_cookie import set_phantomjs, get_cookie_dict
from .static_json import dump as dump_static_json
