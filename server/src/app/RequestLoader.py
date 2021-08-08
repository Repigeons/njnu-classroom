#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/22
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import Request

from exceptions import RequestParameterError


class RequestLoader:
    @classmethod
    async def load(cls, request: Request):
        self = cls()
        self.request = request
        self.headers = request.headers
        self.query = request.query
        if request.method == 'GET':
            return self
        if request.content_type[:len('application/json')] == 'application/json':
            self.json = await request.json()
        else:
            self.data = await request.post()
        return self

    def __init__(self):
        self.request = None
        self.headers = None
        self.query = None
        self.json = None
        self.data = None

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
