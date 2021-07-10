#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  Zhou Tianxing
# @Software :  PyCharm x64
""""""
import datetime
import json

from aiohttp.web import json_response, FileField, Request, Response

from app import app
from ztxlib import aioredis
from .routes import routes
from ..service import ShuttleService


@routes.get('/shuttle.json')
async def shuttle(request: Request) -> Response:
    async with aioredis.start(app['redis']) as redis:
        data = await redis.hget(
            "shuttle",
            str(datetime.datetime.now().weekday())
        )
        data = json.loads(await redis.hget(
            "shuttle",
            str(datetime.datetime.now().weekday())
        ))
    return json_response(
        data,
        status=200
    )


@routes.post('/shuttle/upload')
async def upload(request: Request) -> Response:
    file: FileField = (await request.post())['file']
    await ShuttleService.email_file(
        content=file.file.read(),
        subject=f"【南师教室】有人上传校车时刻表.{file.filename.split('.')[-1]}",
    )
    return json_response(
        dict(),
        status=200
    )
