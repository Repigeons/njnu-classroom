#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Email.py
""""""
import json

from ._smtp import SMTP

mail_config = json.load(open('conf/mail.json'))

__mail_server = SMTP(**mail_config)


def __send_email(subject: str, message: str):
    __mail_server.send(
        subject, message, 'plain',
        'Repigeons<zz.daniel@foxmail.com>',
        {'name': 'Zhou T.x.', 'addr': 'z.t.x@foxmail.com'},
        {'name': 'ZzDaniel', 'addr': 'zz.daniel@foxmail.com'},
        {'name': 'Wang Fusheng', 'addr': '739286973@qq.com'},
    )
