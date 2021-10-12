#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
import logging
import time
from json.decoder import JSONDecodeError

import aiohttp

from app import app
from ztxlib import aioredis


async def save_time() -> None:
    """
    将时间信息保存至Redis
    """
    try:
        async with aioredis.start(app['redis']) as redis:
            cookies = json.loads(await redis.hget("spider", "cookies"))
        logging.info("开始查询时间信息...")
        time_info = await get_time_info(cookies=cookies)
        logging.info("时间信息查询成功")
        async with aioredis.start(app['redis']) as redis:
            await redis.hset("spider", "time_info", json.dumps(time_info))
        logging.info("时间信息存储完成")

    except JSONDecodeError as e:
        app['mail'](
            subject="【南师教室】错误报告",
            content=f"cookies无效\n"
                    f"JSONDecodeError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.critical("cookies无效")
        logging.info("Exit with code %d", 2)
        exit(2)

    except KeyError as e:
        app['mail'](
            subject="【南师教室】错误报告",
            content=f"获取时间信息失败\n"
                    f"KeyError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.critical("获取时间信息失败")
        logging.info("Exit with code %d", 3)
        exit(3)

    except Exception as e:
        app['mail'](
            subject="【南师教室】错误报告",
            content=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.critical(f"{type(e), e}")
        logging.info("Exit with code %d", -1)
        exit(-1)


async def get_time_info(cookies: dict) -> dict:
    """
    获取时间相关信息
    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :return:dict{学年学期代码, 学年代码, 学期代码, 周次, 总周次, 总教学周次}
    """
    result = {}

    # 查询当前学年学期
    async with aiohttp.request(
            method="POST",
            url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do',
            cookies=cookies
    ) as resp:
        res = await resp.json(content_type=None)
    result['XNXQDM'] = res['datas']['cxdqxnxq']['rows'][0]['DM'],
    result['XNDM'] = res['datas']['cxdqxnxq']['rows'][0]['XNDM'],
    result['XQDM'] = res['datas']['cxdqxnxq']['rows'][0]['XQDM']

    # 查询当前周次和总周次
    async with aiohttp.request(
            method="POST",
            url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do',
            cookies=cookies,
            data=dict(
                XN=result['XNDM'],
                XQ=result['XQDM'],
                RQ=time.strftime("%Y-%m-%d", time.localtime()),
            )
    ) as resp:
        res = await resp.json(content_type=None)
    result['ZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZC']
    result['ZZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZZC']

    # 查询总教学周次
    async with aiohttp.request(
            method="POST",
            url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do',
            cookies=cookies,
            data=dict(
                XN=result['XNDM'],
                XQ=result['XQDM'],
                SFSY=1,
            )
    ) as resp:
        res = await resp.json(content_type=None)
    result['ZJXZC'] = res['datas']['cxxljc']['rows'][0]['ZJXZC']

    return result
