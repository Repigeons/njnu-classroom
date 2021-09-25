#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  Zhou Tianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import Request

from app import *
from .routes import routes
from ..service import EmptyService, FeedbackService


@routes.get('/empty.json')
async def empty(request: Request) -> JsonResponse:
    if not app['config']['service']:
        return JsonResponse(
            status=HttpStatus.IM_A_TEAPOT,
            message="service off",
            data=[],
        )

    request = await RequestLoader.load(request)
    jxl = request.args(name='jxl', typing=str)
    day = request.args(name='day', typing=int)
    dqjc = request.args(name='dqjc', typing=int)

    result = await EmptyService.handle(jxl, day, dqjc)
    return JsonResponse(data=result)


@routes.post('/feedback')
async def feedback(request: Request) -> JsonResponse:
    if not app['config']['service']:
        return JsonResponse(
            status=HttpStatus.IM_A_TEAPOT,
            message="service off",
        )

    request = await RequestLoader.load(request)
    jc = request.json(name='jc', typing=int)
    results = request.json(name='results', typing=list)
    index = request.json(name='index', typing=int)
    jxlmc = request.json(name='jxl', typing=str)
    day = request.json(name='day', typing=int)

    await FeedbackService.handle(jc, results, index, jxlmc, day)
    return JsonResponse(status=HttpStatus.ACCEPTED)
