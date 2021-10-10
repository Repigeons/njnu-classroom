#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import Request

from app import JsonResponse, HttpStatus, initialize
from .routes import routes
from ..service import ResetService


@routes.post('/reset')
async def reset(_: Request) -> JsonResponse:
    await ResetService.reset()
    return JsonResponse(status=HttpStatus.ACCEPTED)


@routes.post('/init')
async def reset(_: Request) -> JsonResponse:
    await initialize()
    return JsonResponse(status=HttpStatus.ACCEPTED)
