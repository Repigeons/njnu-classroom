#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  Zhou Tianxing
# @Software :  PyCharm x64
""""""
import logging

from aiohttp.web import Request

from app import app, JsonResponse, HttpStatus
from .routes import routes
from ..service import IndexService

config = app['config']['application']['notice']


@routes.put('/')
async def index(request: Request) -> JsonResponse:
    token = request.headers.get('token')
    data = await request.post()
    text = data['text']
    if not isinstance(token, str) or token != config['token']:
        return JsonResponse(
            status=HttpStatus.FORBIDDEN,
            message="TokenError",
        )
    elif not isinstance(text, str):
        return JsonResponse(
            status=HttpStatus.BAD_REQUEST,
            message="TextError",
        )

    try:
        data = await IndexService.handle(text)
        return JsonResponse(data=data)
    except Exception as e:
        logging.error(
            f"{type(e), e}"
            f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        return JsonResponse(
            status=HttpStatus.INTERNAL_SERVER_ERROR,
            message=f"{type(e), e}",
        )
