#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_time.py
""""""
import json
import logging
import time
from json.decoder import JSONDecodeError

import aiohttp
from redis import StrictRedis
from ztxlib.rpspring import Autowired


class __Application:
    @Autowired
    def redis_pool(self): pass

    @Autowired
    def send_email(self) -> None: pass


async def save_time() -> None:
    """
    将时间信息保存至Redis
    """
    try:
        redis = StrictRedis(connection_pool=__Application.redis_pool)
        cookies = json.loads(redis.hget("Spider", "cookies"))
        logging.info("开始查询时间信息...")
        time_info = await get_time_info(cookies=cookies)
        logging.info("时间信息查询成功")
        redis.hset("Spider", "time_info", json.dumps(time_info))
        logging.info("时间信息存储完成")
    except JSONDecodeError as e:
        logging.error("cookies无效")
        __Application.send_email(
            subject="【南师教室】错误报告",
            message=f"cookies无效\n"
                    f"JSONDecodeError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 2)
        exit(2)
    except KeyError as e:
        logging.error("获取时间信息失败")
        __Application.send_email(
            subject="【南师教室】错误报告",
            message=f"获取时间信息失败\n"
                    f"KeyError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 3)
        exit(3)
    except Exception as e:
        logging.error(f"{type(e), e}")
        __Application.send_email(
            subject="【南师教室】错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
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
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do',
                cookies=cookies
        ) as resp:
            res = await resp.json()
    result['XNXQDM'] = res['datas']['cxdqxnxq']['rows'][0]['DM'],
    result['XNDM'] = res['datas']['cxdqxnxq']['rows'][0]['XNDM'],
    result['XQDM'] = res['datas']['cxdqxnxq']['rows'][0]['XQDM']

    # 查询当前周次和总周次
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do',
                cookies=cookies,
                data=dict(
                    XN=result['XNDM'],
                    XQ=result['XQDM'],
                    RQ=time.strftime("%Y-%m-%d", time.localtime()),
                )
        ) as resp:
            res = await resp.json()
    result['ZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZC']
    result['ZZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZZC']

    # 查询总教学周次
    async with aiohttp.ClientSession() as session:
        async with session.post(
                url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do',
                cookies=cookies,
                data=dict(
                    XN=result['XNDM'],
                    XQ=result['XQDM'],
                    SFSY=1,
                )
        ) as resp:
            res = await resp.json()
    result['ZJXZC'] = res['datas']['cxxljc']['rows'][0]['ZJXZC']

    return result
