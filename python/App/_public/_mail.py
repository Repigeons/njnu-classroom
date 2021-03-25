#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/25
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _mail.py
""""""
from email.mime.text import MIMEText
from threading import Thread

from utils import SMTP
from utils.aop import bean, configuration


@configuration("mail.sender")
def sender(): pass


@configuration("mail.receivers")
def receivers(): pass


@bean()
def send_email():
    server = SMTP(**sender)

    def send(subject: str, message: str):
        Thread(
            target=server.send,
            kwargs={
                'subject': subject,
                'header_from': "Repigeons",
                'header_to': "南师教室运维人员",
                'receivers': [receiver['addr'] for receiver in receivers],
                'mime_parts': [MIMEText(message)]
            }
        ).start()

    return send
