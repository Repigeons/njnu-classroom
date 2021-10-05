#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import Request

from app import *
from .routes import routes
from ..service import OverviewService


@routes.get('/overview.json')
async def overview(request: Request) -> JsonResponse:
    if not app['config']['service']:
        return JsonResponse(
            status=HttpStatus.IM_A_TEAPOT,
            message="service off",
            data=[],
        )

    request = await RequestLoader.load(request)
    jasdm = request.args(name='jasdm', typing=str)

    result = await OverviewService.handle(jasdm)
    return JsonResponse(data=result)
