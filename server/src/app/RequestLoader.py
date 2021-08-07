#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/22
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp import web

from exceptions import RequestParameterError


class RequestLoader:
    def __init__(self, request: web.Request):
        self.request = request
        self.headers = request.headers
        self.query = request.query
        self.json = yield from request.json()
        self.data = yield from request.post()

    @staticmethod
    def __verify(value, name: str, typing: type, nullable: bool, default):
        if value is None:
            if nullable or default is not None:
                return default
            if typing is not None:
                raise RequestParameterError(name)
        if typing is None:
            return value
        if typing is bool:
            return str(value).lower() == str(True).lower()
        if isinstance(value, str) and typing in (set, tuple, list, iter):
            value = value.split(',')
        try:
            return typing(value)
        except ValueError:
            raise RequestParameterError(name)

    def header(self,
               name: str,
               typing: type = None,
               nullable: bool = None,
               default=None):
        value = self.headers.get(name)
        return self.__verify(value, name, typing, nullable, default)

    def args(self,
             name: str,
             typing: type = None,
             nullable: bool = None,
             default=None):
        value = self.query.get(name)
        return self.__verify(value, name, typing, nullable, default)

    def json(self,
             name: str,
             typing: type = None,
             nullable: bool = None,
             default=None):
        value = self.json.get(name)
        return self.__verify(value, name, typing, nullable, default)

    def form(self,
             name: str,
             typing: type = None,
             nullable: bool = None,
             default=None):
        value = self.data.get(name)
        return self.__verify(value, name, typing, nullable, default)
