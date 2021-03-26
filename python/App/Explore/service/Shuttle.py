#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
import csv
import json

from redis import StrictRedis
from redis_lock import Lock

from App.Explore import dao
from utils.aop import autowired


@autowired()
def redis_pool(): pass


def reset():
    redis = StrictRedis(connection_pool=redis_pool)
    lock = Lock(redis, "Explore-Shuttle")
    if lock.acquire(blocking=False):
        try:
            with open("resources/stations.csv", encoding='utf8') as f:
                stations = [
                    {
                        'name': row['name'],
                        'position': [
                            float(row['latitude']),
                            float(row['longitude'])
                        ]
                    }
                    for row in csv.DictReader(f)
                ]
                f.close()
            redis.delete("Shuttle")
            for day in range(7):  # [monday, ..., sunday]
                direction1, direction2 = [], []
                for row in dao.get_shuttles(day=1 << 6 >> day, route=1):
                    for i in range(row.shuttle_count):
                        direction1.append([row.start_time, row.start_station, row.end_station])
                for row in dao.get_shuttles(day=1 << 6 >> day, route=2):
                    for i in range(row.shuttle_count):
                        direction2.append([row.start_time, row.start_station, row.end_station])
                redis.hset(
                    name="Shuttle",
                    key=str(day),
                    value=json.dumps(({
                        'direction1': direction1,
                        'direction2': direction2,
                        'stations': stations
                    }))
                )
        finally:
            lock.release()
