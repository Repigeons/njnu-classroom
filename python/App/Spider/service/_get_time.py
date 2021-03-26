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

import requests
from redis import StrictRedis

from utils.aop import autowired


@autowired()
def redis_pool(): pass


@autowired()
def send_email(subject: str, message: str): _ = subject, message


def save_time() -> None:
    """
    将时间信息保存至Redis
    """
    try:
        redis = StrictRedis(connection_pool=redis_pool)
        cookies = json.loads(redis.hget("Spider", "cookies"))
        logging.info("开始查询时间信息...")
        time_info = get_time_info(cookies=cookies)
        logging.info("时间信息查询成功")
        redis.hset("Spider", "time_info", json.dumps(time_info))
        logging.info("时间信息存储完成")
    except JSONDecodeError as e:
        logging.error("cookies无效")
        send_email(
            subject="南师教室：错误报告",
            message=f"cookies无效\n"
                    f"JSONDecodeError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 2)
        exit(2)
    except KeyError as e:
        logging.error("获取时间信息失败")
        send_email(
            subject="南师教室：错误报告",
            message=f"获取时间信息失败\n"
                    f"KeyError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 3)
        exit(3)
    except Exception as e:
        logging.error(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", -1)
        exit(-1)


def get_time_info(cookies: dict) -> dict:
    """
    获取时间相关信息
    :param cookies:dict{MOD_AUTH_CAS, _WEU}
    :return:dict{学年学期代码, 学年代码, 学期代码, 周次, 总周次, 总教学周次}
    """
    result = {}

    # 查询当前学年学期
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxdqxnxq.do',
        cookies=cookies
    ).json()
    result['XNXQDM'] = res['datas']['cxdqxnxq']['rows'][0]['DM'],
    result['XNDM'] = res['datas']['cxdqxnxq']['rows'][0]['XNDM'],
    result['XQDM'] = res['datas']['cxdqxnxq']['rows'][0]['XQDM']

    # 查询当前周次和总周次
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxrqdydzcxq.do',
        cookies=cookies,
        data={
            'XN': result['XNDM'],
            'XQ': result['XQDM'],
            'RQ': time.strftime("%Y-%m-%d", time.localtime())
        }
    ).json()
    result['ZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZC']
    result['ZZC'] = res['datas']['cxrqdydzcxq']['rows'][0]['ZZC']

    # 查询总教学周次
    res = requests.post(
        url='http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/modules/jsjysq/cxxljc.do',
        cookies=cookies,
        data={
            'XN': result['XNDM'],
            'XQ': result['XQDM'],
            'SFSY': 1
        }
    ).json()
    result['ZJXZC'] = res['datas']['cxxljc']['rows'][0]['ZJXZC']

    return result
