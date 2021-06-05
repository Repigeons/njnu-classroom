#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/13 0013
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
import datetime
import json

from flask import current_app as app, jsonify
from redis import StrictRedis
from redis_lock import Lock
from ztxlib.rpspring import Autowired


class __Application:
    @Autowired
    def redis_pool(self): pass


@app.route('/shuttle.json', methods=['GET'])
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
