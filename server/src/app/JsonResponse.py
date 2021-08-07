#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/21
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
from enum import Enum, unique

from aiohttp import web


@unique
class HttpStatus(Enum):
    # 2xx
    SUCCESS = 200
    ACCEPTED = 202
    # 4xx
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    IM_A_TEAPOT = 418
    # 5xx
    INTERNAL_SERVER_ERROR = 500


class JsonResponse(web.Response):
    def __init__(self, *,
                 status: HttpStatus = HttpStatus.SUCCESS,
                 message: str = None,
                 data=None,
                 ):
        if not isinstance(status, HttpStatus):
            raise TypeError(status, type(status), HttpStatus)
        super().__init__(
            status=status.value,
            text=json.dumps(dict(
                status=status.value,
                message=message,
                data=data
            )),
            content_type="application/json",
        )
