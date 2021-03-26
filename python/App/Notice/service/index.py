#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  index.py
""""""
import datetime
import json
import os
from typing import Dict, Union

from utils.aop import configuration


@configuration("application.notice.token")
def token(): pass


@configuration("application.notice.file")
def notice_file(): pass


def handle(form_data: dict, headers: dict) -> Dict[str, Union[int, str, dict]]:
    if 'text' not in form_data.keys():
        raise KeyError("Expected field `text`")
    if 'HTTP_TOKEN' not in headers.keys():
        raise KeyError("Expected field `token`")
    if token != headers['HTTP_TOKEN']:
        raise ValueError("Invalid token")

    # Save to notice history
    if os.path.exists(notice_file):
        file = os.path.abspath(notice_file)
        history = os.path.join(os.path.dirname(file), f"_{os.path.basename(file)}")
        history_list = json.load(open(history, encoding='utf8')) if os.path.exists(history) else []
        history_list.append(json.load(open(file, encoding='utf8')))
        json.dump(history_list, open(history, 'w', encoding='utf8'))

    # Save to [notice.json]
    text: str = form_data['text']
    for ch in [('\\n', '\n')]:
        text = text.replace(*ch)
    now = datetime.datetime.now()
    data = {
        'timestamp': int(now.timestamp()),
        'date': now.strftime("%Y-%m-%d"),
        'text': text,
    }
    json.dump(
        obj=data,
        fp=open(notice_file, 'w', encoding='utf8'),
        ensure_ascii=False,
        indent=2
    )
    return {
        'status': 0,
        'message': "ok",
        'data': data
    }
