#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/4/21
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _email.py
""""""
from email.mime.text import MIMEText
from threading import Thread

from ztxlib.rpspring import Bean
from ztxlib.rpspring import Value
from ztxlib.smtp import SMTP


@Value("mail.sender")
def config() -> dict: pass


@Value("mail.receivers")
def receivers() -> list: pass


@Bean
class SendEmail:
    def __init__(self):
        self.smtp = SMTP(**config)

    def __call__(self, subject: str, message: str):
        Thread(
            target=self.smtp.send,
            kwargs={
                'subject': subject,
                'header_from': "Repigeons",
                'header_to': "南师教室运维人员",
                'receivers': [receiver['addr'] for receiver in receivers],
                'mime_parts': [MIMEText(message)]
            }
        ).start()
