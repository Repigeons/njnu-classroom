#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/13 0013
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
import datetime
import json

from flask import current_app as app
from flask import jsonify
from flask import request
from redis import StrictRedis
from redis_lock import Lock
from ztxlib.rpspring import Autowired

from App.Explore.service import EmailFile


class __Application:
    @Autowired
    def redis_pool(self): pass


@app.get('/shuttle.json')
def shuttle():
    redis = StrictRedis(connection_pool=__Application.redis_pool)
    lock = Lock(redis, "Explore-Shuttle")
    if lock.acquire():
        try:
            return jsonify(json.loads(redis.hget(
                "Shuttle",
                str(datetime.datetime.now().weekday())
            )))
        finally:
            lock.release()


@app.post('/shuttle/upload')
def upload():
    file = request.files.get('file')
    EmailFile.email_file(
        content=file.stream.read(),
        subject=f"【南师教室】有人上传校车时刻表.{file.filename.split('.')[-1]}",
    )
    return jsonify(
        status=0
    )
