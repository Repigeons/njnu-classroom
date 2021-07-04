#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Connections
""""""
from ztxlib.rpspring import Value


class Context:
    @Value("database.mysql")
    def mysql(self): pass


connections = None
if Context.mysql is not None:
    from ztxlib.mariadb import MariaDB

    connections = MariaDB(**Context.mysql)
