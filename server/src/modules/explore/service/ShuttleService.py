#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import csv
import json
from email.mime.application import MIMEApplication

from app import app
from ztxlib import *

day_mapper = {
    0: 'Mon.',
    1: 'Tue.',
    2: 'Wed.',
    3: 'Thu.',
    4: 'Fri.',
    5: 'Sat.',
    6: 'Sun.',
}


async def reset():
    try:
        async with aioredis.lock(app['redis'], 'explore-shuttle', 0):
            with open("resources/stations.csv", encoding='utf8') as f:
                stations = [
                    dict(
                        name=row['name'],
                        position=[
                            float(row['latitude']),
                            float(row['longitude'])
                        ]
                    ) for row in csv.DictReader(f)
                ]
            mysql: aiomysql.MySQL = app['mysql']
            for day_of_week in range(7):
                direction1, direction2 = [], []
                rows1 = await mysql.fetchall(
                    "SELECT * FROM `shuttle` WHERE (`working`& %(day)s) AND `route`=%(route)s",
                    dict(
                        day=1 << 6 >> day_of_week,
                        route=1
                    )
                )
                rows2 = await mysql.fetchall(
                    "SELECT * FROM `shuttle` WHERE (`working`& %(day)s) AND `route`=%(route)s",
                    dict(
                        day=1 << 6 >> day_of_week,
                        route=2
                    )
                )
                for row in rows1:
                    for i in range(row['shuttle_count']):
                        direction1.append([row['start_time'], row['start_station'], row['end_station']])
                for row in rows2:
                    for i in range(row['shuttle_count']):
                        direction2.append([row['start_time'], row['start_station'], row['end_station']])
                async with aioredis.start(app['redis']) as redis:
                    await redis.hset(
                        name="shuttle",
                        key=day_mapper[day_of_week],
                        value=json.dumps(({
                            'direction1': direction1,
                            'direction2': direction2,
                            'stations': stations
                        }))
                    )

    except aioredis.exceptions.WaitingTimeoutError:
        pass


async def email_file(
        content: bytes,
        subject: str
):
    mime = MIMEApplication(content)
    mime.add_header('Content-Disposition', 'attachment', filename=subject)
    app['mail'](
        subject=subject,
        mime_parts=[mime]
    )
