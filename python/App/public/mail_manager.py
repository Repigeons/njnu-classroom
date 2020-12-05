#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  mail_manager.py
""""""
import json

from utils import SMTP, Threading

__mail_config = json.load(open('conf/mail.json'))

__mail_server = SMTP(**__mail_config['sender'])


def send_email(subject: str, message: str):
    def _send(_subject: str, _message: str):
        __mail_server.send(
            subject, message, 'plain',
            'Repigeons<info@njnu.xyz>',
            *__mail_config['receivers']
        )

    Threading(_send).start(_subject=subject, _message=message)
