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
from typing import Optional

from app import app

config = app['config']['application']['notice']


async def put(text: str) -> dict:
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


async def rollback() -> Optional[dict]:
    file = os.path.abspath(config['file'])
    history = os.path.join(os.path.dirname(file), f"_{os.path.basename(file)}")
    if os.path.exists(history):
        with open(history, 'rb') as f:
            notices = json.load(f)
        with open(history, 'w') as f:
            json.dump(notices[:-1], f)
        with open('notice.json', 'w') as f:
            json.dump(notices[-1], f, ensure_ascii=False, indent=2)
        return notices[-1]
    return None
