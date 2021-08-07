#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import Request

from app import *
from .routes import routes
from ..service import SearchService


@routes.get('/search.json')
async def search(request: Request) -> JsonResponse:
    if not app['config']['application']['server']['service']:
        return JsonResponse(
            status=HttpStatus.IM_A_TEAPOT,
            message="service off",
            data=[],
        )

    request = RequestLoader(request)
    day = request.args(name='day', typing=str, default='#')
    jc_ks = request.args(name='jc_ks', typing=int, default=1)
    jc_js = request.args(name='jc_js', typing=int, default=12)
    jxl = request.args(name='jxl', typing=str, default='#')
    zylxdm = request.args(name='zylxdm', typing=str, default='#')
    keyword = request.args(name='kcm', typing=str, default='#')

    result = await SearchService.handle(day, jc_ks, jc_js, jxl, zylxdm, keyword)
    return JsonResponse(data=result)
