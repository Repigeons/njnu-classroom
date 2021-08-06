#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json

from aiohttp.web import json_response, Request, Response

from app import app
from .routes import routes
from ..service import FeedbackService


@routes.post('/feedback')
async def feedback(request: Request) -> Response:
    if not app['config']['application']['server']['service']:
        return json_response(
            dict(),
            status=403
        )

    form_data = await request.json()

    await FeedbackService.handle(
        jc=form_data['jc'],
        results=json.loads(form_data['results']),
        index=int(form_data['index']),
        jxlmc=form_data['jxl'],
        day=int(form_data['day'])
    )
    return json_response(
        dict(
            status=0,
            message="ok",
            data=None
        ),
        status=202
    )
