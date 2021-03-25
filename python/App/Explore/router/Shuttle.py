#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/13 0013
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
import csv
import datetime
import json

from flask import current_app as app, jsonify
from redis import StrictRedis
from redis_lock import Lock

from utils.aop import autowired


@autowired()
def mysql(): pass


@autowired()
def redis_pool(): pass


@app.route('/shuttle.json', methods=['GET'])
def shuttle():
    redis = StrictRedis(connection_pool=redis_pool)
    lock = Lock(redis, "Explore-Shuttle")
    if lock.acquire():
        try:
            return jsonify(json.loads(redis.hget(
                "Shuttle",
                str(datetime.datetime.now().weekday())
            )))
        finally:
            lock.release()


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
                connection, cursor = mysql.get_connection_cursor()
                try:
                    cursor.execute(
                        "SELECT * FROM `shuttle` WHERE (`working`& %(day)s) AND `route`=1",
                        {'day': 1 << 6 >> day}
                    )
                    for row in cursor.fetchall():
                        for i in range(row.shuttle_count):
                            direction1.append([row.start_time, row.start_station, row.end_station])
                    cursor.execute(
                        "SELECT * FROM `shuttle` WHERE (`working`& %(day)s) AND `route`=2",
                        {'day': 1 << 6 >> day}
                    )
                    for row in cursor.fetchall():
                        for i in range(row.shuttle_count):
                            direction2.append([row.start_time, row.start_station, row.end_station])
                finally:
                    cursor.close(), connection.close()
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


reset()
