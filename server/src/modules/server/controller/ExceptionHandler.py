#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from email.mime.text import MIMEText

from aiohttp.web import json_response

from .middlewares import middlewares


@middlewares.append
async def middleware(app, http_handler):
    async def handler(request):
        try:
            return await http_handler(request)
        except Exception as e:
            async with app['smtp'] as smtp:
                await smtp.send(
                    **app['mail'],
                    subject="【南师教室】错误报告",
                    mime_parts=[MIMEText(
                        f"{type(e), e}\n"
                        f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
                    )])
            return json_response(
                dict(
                    status=-1,
                    message=f"{type(e), e}",
                    data=None
                ),
                status=400
            )

    return handler
