#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _get_cookie
""""""
from selenium import webdriver

__phantomjs = 'phantomjs'


def set_phantomjs(phantomjs: str):
    global __phantomjs
    __phantomjs = phantomjs


def get_cookie_dict(account: dict) -> dict:
    """
    模拟登录，获取所需的cookie

    :param account:dict{username, password, gid}
    :return:dict{_WEU, MOD_AUTH_CAS}
    """
    global __phantomjs
    username, password, gid = account.values()

    browser = webdriver.PhantomJS(__phantomjs)
    url = 'http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/*default/index.do?amp_sec_version_=1&gid_=' + gid
    browser.get(url)

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
