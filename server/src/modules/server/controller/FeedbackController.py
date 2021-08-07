#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import Request

from app import *
from .routes import routes
from ..service import FeedbackService


@routes.post('/feedback')
async def feedback(request: Request) -> JsonResponse:
    if not app['config']['application']['server']['service']:
        return JsonResponse(
            status=HttpStatus.IM_A_TEAPOT,
            message="service off",
        )

    request = await RequestLoader.load(request)
    jc = request.json(name='jc', typing=int)
    results = request.json(name='results', typing=list)
    index = request.json(name='index', typing=int)
    jxlmc = request.json(name='jxlmc', typing=str)
    day = request.json(name='day', typing=int)

    await FeedbackService.handle(jc, results, index, jxlmc, day)
    return JsonResponse(status=HttpStatus.ACCEPTED)
