#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _connections.py
""""""
from .. import MariaDB
from .. import value


@value("database.mysql")
def config(): pass


connections = MariaDB(**config)
