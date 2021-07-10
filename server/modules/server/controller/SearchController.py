#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from aiohttp.web import json_response, Request, Response

from app import app
from .routes import routes
from ..service import SearchService


@routes.get('/search.json')
async def search(request: Request) -> Response:
    if not app['config']['application']['server']['service']:
        return json_response(
            dict(
                status=1,
                message="service off",
                service='off',
                data=[]
            ),
            status=200
        )

    try:
        result = await SearchService.handle(dict(request.query))
        return json_response(
            dict(
                status=0,
                message="ok",
                service='on',
                data=result
            ),
            status=200
        )

    except KeyError as e:
        return json_response(
            dict(
                status=2,
                message=f"Expected or unresolved key [{e}]",
                data=[]
            ),
            status=400
        )
