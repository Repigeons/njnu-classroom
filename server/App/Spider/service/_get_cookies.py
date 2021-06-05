#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_cookies.py
""""""
import json
import logging
from json.decoder import JSONDecodeError

from redis import StrictRedis
from selenium import webdriver
from ztxlib.rpspring import Autowired
from ztxlib.rpspring import Value


class __Application:
    @Autowired
    def redis_pool(self): pass

    @Autowired
    def send_email(self) -> None: pass

    @Value("application.spider.account")
    def account(self): pass

    @Value("application.spider.selenium")
    def selenium(self): pass


def save_cookies() -> None:
    """
    将cookies内容保存至Redis
    """
    try:
        redis = StrictRedis(connection_pool=__Application.redis_pool)
        logging.info("开始尝试获取cookies...")
        cookies = get_cookie_dict()
        logging.info("cookies获取成功")
        redis.hset("Spider", "cookies", json.dumps(cookies))
        logging.info("cookies存储完成")
    except FileNotFoundError as e:
        logging.error("配置文件缺失")
        __Application.send_email(
            subject="南师教室：错误报告",
            message=f"配置文件缺失\n"
                    f"FileNotFoundError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 1)
        exit(1)
    except JSONDecodeError as e:
        logging.error("配置文件解析失败")
        __Application.send_email(
            subject="南师教室：错误报告",
            message=f"配置文件解析失败\n"
                    f"JSONDecodeError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 1)
        exit(1)
    except KeyError as e:
        logging.error("登录失败")
        __Application.send_email(
            subject="南师教室：错误报告",
            message=f"登录失败\n"
                    f"KeyError\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", 1)
        exit(1)
    except Exception as e:
        logging.error(f"{type(e), e}")
        __Application.send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        logging.info("Exit with code %d", -1)
        exit(-1)


def get_cookie_dict() -> dict:
    """
    模拟登录，获取所需cookie
    :return:dict{_WEU, MOD_AUTH_CAS}
    """
    username, password, gid = __Application.account.values()
    driver = __Application.selenium['driver']
    args = __Application.selenium['list'][driver]

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

        cookie = {item['name']: item['value'] for item in browser.get_cookies()}

        return {
            'MOD_AUTH_CAS': cookie['MOD_AUTH_CAS'],
            '_WEU': cookie['_WEU']
        }
    finally:
        browser.close()
        browser.quit()
