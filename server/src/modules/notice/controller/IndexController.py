#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  Zhou Tianxing
# @Software :  PyCharm x64
""""""
import logging

import aiofiles
from aiohttp.web import View, Response

from app import *
from .routes import routes
from ..service import IndexService

config = app['config']['application']['notice']


@routes.view('/')
class NoticeView(View):
    @staticmethod
    async def get():
        async with aiofiles.open("resources/notice.html", 'rb') as f:
            return Response(
                body=await f.read(),
                content_type='text/html',
            )

    async def put(self):
        request = await RequestLoader.load(self.request)
        token = request.header('token', str)
        text = request.form('text', str)
        if token != config['token']:
            return JsonResponse(
                status=HttpStatus.FORBIDDEN,
                message="TokenError",
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
