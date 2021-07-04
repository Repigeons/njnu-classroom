#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Context
""""""
import os

import yaml

from ._SingletonException import SingletonException


class ApplicationContext:
    _beans = {}
    _configurations = {}

    if os.path.exists("resources/application.yml"):
        with open("resources/application.yml") as f:
            _configurations.update(yaml.safe_load(f))

    def __init__(self):
        raise SingletonException(ApplicationContext)

    @classmethod
    def add_bean(cls, bean_name: str, bean_object: any):
        cls._beans.update({
            bean_name: bean_object
        })

    @classmethod
    def get_bean(cls, bean_name: str):
        return cls._beans.get(bean_name) if bean_name in cls._beans else None

    @classmethod
    def get_configuration(cls, name: str):
        name = name.split('.')
        config = cls._configurations
        for key in name:
            if key not in config.keys():
                return None
            config = config[key]
        return config
