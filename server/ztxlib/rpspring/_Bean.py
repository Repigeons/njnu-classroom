#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _Bean
""""""
import inspect
import re

from ._Context import ApplicationContext


class Bean:
    def __new__(cls, bean_definition):
        # name = bean_definition.__name__
        name = re.sub(r"([A-Z])", lambda v: f"_{v.group(1).lower()}", bean_definition.__name__)
        if name[0] == '_':
            name = name[1:]
        spec = inspect.getfullargspec(bean_definition)
        kwargs = {}
        spec_args = []
        if spec.defaults is not None:
            spec_defaults = spec.defaults
            spec_args = spec.args[-len(spec_defaults)]
            kwargs = {
                spec_args[i]: spec_defaults[i]
                for i in range(len(spec_args))
            }
        kwargs.update({arg: None for arg in spec.args if arg not in spec_args})
        if isinstance(bean_definition, type) and 'self' in spec.args:
            kwargs.pop('self')
        bean = bean_definition(**kwargs)
        ApplicationContext.add_bean(name, bean)
        return bean_definition
