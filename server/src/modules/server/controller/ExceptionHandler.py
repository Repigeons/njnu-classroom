#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""

from aiohttp.web_exceptions import HTTPClientError

from app import JsonResponse, HttpStatus
from exceptions import RequestParameterError
from .middlewares import middlewares


@middlewares.append
async def middleware(app, http_handler):
    async def handler(request) -> JsonResponse:
        try:
            return await http_handler(request)
        except RequestParameterError as exception:
            return JsonResponse(
                status=HttpStatus.BAD_REQUEST,
                message="Request parameter error: [%s]" % exception.args[0],
            )
        except HTTPClientError as exception:
            raise exception
        except Exception as e:
            await app['mail'](
                subject="【南师教室】错误报告",
                content=f"{type(e), e}\n"
                        f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
            )
            return JsonResponse(
                status=HttpStatus.INTERNAL_SERVER_ERROR,
                message=f"{type(e), e}",
            )

    return handler
