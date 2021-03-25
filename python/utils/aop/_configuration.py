#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/24
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _configuration.py
""""""
import logging
import os

import yaml

from ._storage import __config


def configuration(param: str):
    keys = param.split('.')

    def func(f):
        res = __config
        for key in keys:
            if key in res.keys():
                res = res[key]
            else:
                logging.warning(f"Value '{param}' not found.")
                return None
        return res

    return func


def __init__():
    if os.path.exists("resources/application.yml"):
        logging.info("Loading configuration from [application.yml]")
        with open("resources/application.yml") as f:
            __config.update(yaml.safe_load(f))
            f.close()


__init__()
