#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  Zhou Tianxing
# @Software :  PyCharm x64
""""""
import json

from aiohttp.web import Request, FileField

from app import app, JsonResponse
from app.RequestLoader import RequestLoader
from exceptions import RequestParameterError
from ztxlib import aioredis
from .routes import routes
from ..service import ShuttleService


@routes.get('/shuttle.json')
async def shuttle(request: Request) -> JsonResponse:
    request = await RequestLoader.load(request)
    day = request.args('day', str)
    if day not in ShuttleService.day_mapper.values():
        raise RequestParameterError('day')
    async with aioredis.start(app['redis']) as redis:
        data = await redis.hget("shuttle", day)
    return JsonResponse(
        data=json.loads(data)
    )


@routes.post('/shuttle/upload')
async def upload(request: Request) -> JsonResponse:
    request = await RequestLoader.load(request)
    file: FileField = request.form("file")
    await ShuttleService.email_file(
        content=file.file.read(),
        subject=f"【南师教室】有人上传校车时刻表.{file.filename.split('.')[-1]}",
    )
    return JsonResponse()
