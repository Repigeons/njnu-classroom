#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""

from aiohttp.web import Request

from app import JsonResponse, HttpStatus
from .routes import routes
from ..service import ResetService


@routes.post('/reset')
async def reset(request: Request) -> JsonResponse:
    await ResetService.reset()
    return JsonResponse(status=HttpStatus.ACCEPTED)
