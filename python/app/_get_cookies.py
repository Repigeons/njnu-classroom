#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/11/30 0030
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_cookies.py
""""""
import json
from json.decoder import JSONDecodeError

from selenium import webdriver
from utils import send_email

__env = 'phantomjs'


def set_phantomjs(phantomjs: str):
    global __env
    __phantomjs = phantomjs


def save_cookies(file: str) -> None:
    """
    将cookies内容保存至文件
    :param file: cookies文件
    :return: None
    """
    try:
        print('开始尝试获取cookies...')
        json.dump(
            get_cookie_dict(account=json.load(open('conf/account.json'))),
            open(file, 'w')
        )
        print('cookies获取完成...')
    except FileNotFoundError:
        send_email(subject="南师教室：错误报告", message=f"FileNotFoundError\n配置文件缺失\nin app._get_cookie at line 60")
        print('配置文件缺失')
        print('Exit with code', 1)
        exit(1)
    except JSONDecodeError:
        send_email(subject="南师教室：错误报告", message=f"JSONDecodeError\n配置文件解析失败\nin app._get_cookie at line 65")
        print('配置文件解析失败')
        print('Exit with code', 1)
        exit(1)
    except KeyError:
        send_email(subject="南师教室：错误报告", message=f"KeyError\n登录失败\nin app._get_cookie at line 70")
        print('登录失败')
        print('Exit with code', 1)
        exit(1)
    except Exception as e:
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}\nin app._get_cookie at line 75")
        print(type(e), e)
        print('Exit with code', -1)
        exit(-1)


def get_cookie_dict(account: dict) -> dict:
    """
    模拟登录，获取所需cookie
    :param account:dict{username, password, gid}
    :return:dict{_WEU, MOD_AUTH_CAS}
    """
    username, password, gid = account.values()

    browser = webdriver.PhantomJS(__env)
    browser.get(f"http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/*default/index.do?amp_sec_version_=1&gid_={gid}")

    browser.switch_to.default_content()
    text1 = browser.find_element_by_id('username')  # 账号
    text1.send_keys(username)
    text2 = browser.find_element_by_id('password')  # 密码
    text2.send_keys(password)
    browser.find_element_by_class_name('auth_login_btn').click()  # 登录按钮

    cookie = {item['name']: item['value'] for item in browser.get_cookies()}
    browser.close()
    browser.quit()

    return {
        'MOD_AUTH_CAS': cookie['MOD_AUTH_CAS'],
        '_WEU': cookie['_WEU']
    }
