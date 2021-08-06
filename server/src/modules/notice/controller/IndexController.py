#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  Zhou Tianxing
# @Software :  PyCharm x64
""""""
import logging

from aiohttp.web import json_response, Request, Response

from app import app
from .routes import routes
from ..service import IndexService

config = app['config']['application']['notice']


@routes.put('/')
async def index(request: Request) -> Response:
    token = request.headers.get('token')
    data = await request.post()
    text = data['text']
    if not isinstance(token, str) or token != config['token']:
        return json_response(
            dict(
                status=1,
                message="TokenError",
                data=None
            ),
            status=403
        )
    elif not isinstance(text, str):
        return json_response(
            dict(
                status=1,
                message="TextError",
                data=None
            ),
            status=400
        )

    try:
        data = await IndexService.handle(text)
        return json_response(
            dict(
                status=0,
                message="ok",
                data=data
            ),
            status=200
        )
    except Exception as e:
        logging.error(
            f"{type(e), e}"
            f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        return json_response(
            dict(
                status=1,
                message=type(e),
                data=e.args
            ),
            status=500
        )
