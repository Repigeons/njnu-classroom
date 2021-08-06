#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import json
import logging
from email.mime.text import MIMEText

from selenium import webdriver

from app import app
from ztxlib import *


async def save_cookies() -> None:
    """
    将cookies内容保存至Redis
    """
    try:
        logging.info("开始尝试获取cookies...")
        cookies = await get_cookie_dict()
        logging.info("cookies获取成功")
        async with aioredis.start(app['redis']) as redis:
            await redis.hset("spider", "cookies", json.dumps(cookies))
        logging.info("cookies存储完成")

    except KeyError as e:
        async with app['smtp'] as smtp:
            await smtp.send(
                **app['mail'],
                subject="【南师教室】错误报告",
                mime_parts=[MIMEText(
                    f"登录失败\n"
                    f"KeyError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
                )])
        logging.critical("登录失败")
        logging.info("Exit with code %d", 1)
        exit(1)

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


async def get_cookie_dict() -> dict:
    """
    模拟登录，获取所需cookie
    :return:dict{_WEU, MOD_AUTH_CAS}
    """
    config = app['config']['application']['spider']
    username, password, gid = config['account'].values()
    driver = config['selenium']['driver']
    args = config['selenium']['list'][driver]

    if driver.lower() == "phantomjs":
        browser = webdriver.PhantomJS(**args)

    elif driver.lower() == "chrome":
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--no-sandbox")
        option.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(options=option, **args)

    elif driver.lower() == "firefox":
        option = webdriver.FirefoxOptions()
        option.add_argument("-headless")
        browser = webdriver.Firefox(options=option, **args)

    else:
        raise Exception(f"Unresolved selenium driver `{driver}`")

    try:
        browser.get(f"http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/*default/index.do?amp_sec_version_=1&gid_={gid}")

        browser.switch_to.default_content()
        browser.find_element_by_id("username").send_keys(username)
        browser.find_element_by_id("password").send_keys(password)
        browser.find_element_by_id("login_submit").click()

        cookie = {
            item['name']: item['value']
            for item in browser.get_cookies()
        }

        return dict(
            MOD_AUTH_CAS=cookie['MOD_AUTH_CAS'],
            _WEU=cookie['_WEU'],
        )
    finally:
        browser.close()
        browser.quit()
