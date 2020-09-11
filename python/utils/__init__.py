#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  __init__.py
""""""
from ._db_manager import truncate, insert, save_to_pro
from ._get_cookie import get_cookie_dict
from .static_json import dump as dump_static_json
