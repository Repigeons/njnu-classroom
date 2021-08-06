#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import datetime
import json
import os
from json import JSONDecodeError

from app import app

config = app['config']['application']['notice']


async def handle(text: str) -> dict:
    # Save to notice history
    file = os.path.abspath(config['file'])
    if os.path.exists(file):
        history = os.path.join(os.path.dirname(file), f"_{os.path.basename(file)}")
        if os.path.exists(history):
            with open(history, 'rb') as f:
                try:
                    history_list = json.load(f)
                except JSONDecodeError as e:
                    history_list = []
        else:
            history_list = []
        with open(file, 'rb') as f:
            try:
                history_list.append(json.load(f))
            except JSONDecodeError as e:
                print(type(e), e)
        with open(history, 'w', encoding='utf8') as f:
            json.dump(history_list, f)

    # Save to [notice.json]
    for ch in [('\\n', '\n')]:
        text = text.replace(*ch)
    now = datetime.datetime.now()
    data = dict(
        timestamp=int(now.timestamp()),
        date=now.strftime("%Y-%m-%d"),
        text=text,
    )
    with open(file, 'w', encoding='utf8') as f:
        json.dump(
            obj=data,
            fp=f,
            ensure_ascii=False,
            indent=2
        )
    return data
