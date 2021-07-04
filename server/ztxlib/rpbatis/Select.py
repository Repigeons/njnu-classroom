#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/17
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  Select
""""""
import inspect
import json
import logging

from ._Connections import connections
from .Statement import Statement


class Select:
    def __init__(self, statement: str):
        if isinstance(statement, str):
            self.statement = Statement(statement)

    def __call__(self, func):
        spec = inspect.getfullargspec(func)
        kw_args = {}
        if spec.defaults is not None:
            spec_defaults = spec.defaults
            spec_args = spec.args[-len(spec_defaults):]
            kw_args = {
                spec_args[i]: spec_defaults[i]
                for i in range(len(spec_args))
            }

        def select(*args, **kwargs):
            kw_args.update({
                spec.args[index]: arg
                for index, arg in enumerate(args)
            })
            kw_args.update(kwargs)
            kwargs = kw_args

            statement = self.statement.splice(kwargs)
            statement = self.statement.parameterize(statement)

            connection, cursor = connections.get_connection_cursor()
            try:
                cursor.execute(statement, kwargs)
                if len(kwargs):
                    logging.info(
                        "Submit [%s] with parameter:\n%s",
                        cursor.statement,
                        json.dumps(kwargs, ensure_ascii=False)
                    )
                else:
                    logging.info("Submit [%s]", cursor.statement)
                return cursor.fetchall()
            finally:
                cursor.close(), connection.close()

        return select
