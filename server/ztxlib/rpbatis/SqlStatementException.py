#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  SqlStatementException
""""""


class SqlStatementException(Exception):
    def __init__(self, statement):
        super().__init__(f"Statement '{statement}' is invalid.")
