#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from threading import Thread

from aiohttp.web import json_response, Request, Response

from .routes import routes
from ..service import ResetService


@routes.post('/reset')
async def reset(request: Request) -> Response:
    Thread(target=ResetService.reset).start()
    return json_response(
        dict(
            status=0,
            message="ok",
            data=None
        ),
        status=202
    )
