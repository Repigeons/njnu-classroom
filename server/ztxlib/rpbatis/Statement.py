#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Statement
""""""
import re


class Statement:
    def __init__(self, statement: str):
        self.statement = re.sub(
            r"\${(.+?)}",
            lambda v: f"%({v.group(1)})s",
            statement
        )

    def splice(self, splicing: dict) -> str:
        if isinstance(splicing, dict):
            statement = self.statement % splicing
        else:
            statement = self.statement
        return statement

    @staticmethod
    def parameterize(statement: str):
        statement = re.sub(
            r"#{(.+?)}",
            lambda v: f"%({v.group(1)})s",
            statement
        )
        return statement
