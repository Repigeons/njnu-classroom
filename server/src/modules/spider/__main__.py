#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import asyncio
import json
import logging
import os
import time
from email.mime.text import MIMEText

from app import app
from ztxlib import *
from . import service


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize())
    loop.run_until_complete(_main())


async def initialize():
    from app import mail, mysql, redis
    await asyncio.gather(
        mail.initialize(),
        mysql.initialize(),
        redis.initialize(),
    )


async def _main():
    try:
        async with aioredis.lock(app['redis'], "spider", wait_timeout=0):
            async with aioredis.start(app['redis']) as redis:
                await redis.delete("spider")
            logging.info("开始课程信息收集工作...")
            logging.info("初始化工作环境...")

            # 采集基础信息
            await prepare()
            # 采集详细信息
            await core()
            # 校正并归并数据
            await correct_and_merge()
            # 将数据放入生产环境
            if os.getenv("env") == "pro":
                await service.copy_to_pro()

        now = time.time() * 1000
        logging.info(
            "本轮课程信息收集工作成功完成. 共计耗时 %f seconds",
            (int(now) - int(os.getenv("startup_time"))) / 1000
        )

    except aioredis.exceptions.WaitingTimeoutError:
        pass

    except SystemExit or KeyboardInterrupt as e:
        raise e

    except Exception as e:
        async with app['smtp'] as smtp:
            await smtp.send(
                **app['mail'],
                subject="【南师教室】错误报告",
                mime_parts=[MIMEText(
                    f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
                )])
        logging.critical(f"{type(e), e}")
        logging.info("Exit with code %d", -1)
        exit(-1)

    finally:
        async with aioredis.start(app['redis']) as redis:
            await redis.delete("spider")


async def prepare():
    logging.info("开始采集基础信息...")
    task1 = asyncio.create_task(
        service.save_cookies(),
    )
    task2 = asyncio.gather(
        service.save_time(),
        service.save_classrooms(),
    )
    await task1
    await task2
    logging.info("基础信息采集完成")


async def core():
    logging.info("开始采集详细信息...")
    async with aioredis.start(app['redis']) as redis:
        cookies = json.loads(await redis.hget("spider", "cookies"))
        time_info = json.loads(await redis.hget("spider", "time_info"))
        classrooms = json.loads(await redis.hget("spider", "classrooms"))
    mysql: aiomysql.MySQL = app['mysql']
    await mysql.execute("TRUNCATE TABLE `KCB`")
    for jxl in classrooms:
        logging.info("开始查询教学楼[%s]...", jxl)
        for classroom in classrooms[jxl]:
            logging.info("正在查询教室[%s %s]...", classroom['JXLMC'], classroom['jsmph'])
            result = await service.get_data(cookies=cookies, time_info=time_info, classroom=classroom)
            await service.save_data(result)
    logging.info("详细信息采集完成")


async def correct_and_merge():
    # 校正数据
    logging.info("开始校正数据...")
    await service.copy_to_dev()
    await service.correct()
    logging.info("校正数据完成")

    # 归并数据
    logging.info("开始归并数据...")
    await service.merge()
    logging.info("归并数据完成")
