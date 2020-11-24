#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/7/17 0017
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _smtp.py
""""""
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL


class SMTP:
    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
    ):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password

    def send(
            self,
            subject: str,
            message: str,
            message_type: str = 'plain',
            header_from: str = '',
            *header_to: dict
    ):
        """
        Send An Email
        :param subject: 邮件标题
        :param message: 邮件内容
        :param message_type: 邮件格式（plain/html）
        :param header_from: 发件人
        :param header_to: 收件人: List<dict> [{'name':'', 'addr':''}, ...]
        :return: None
        """
        smtp = SMTP_SSL(host=self.__host)
        smtp.connect(host=self.__host, port=self.__port)
        smtp.login(user=self.__user, password=self.__password)
        message = MIMEText(message, message_type, 'utf-8')
        message['Subject'] = Header(subject)
        message['From'] = Header(header_from)
        message['To'] = Header(';'.join(['%(name)s<%(addr)s>' % to for to in header_to]))
        smtp.sendmail(
            from_addr=self.__user,
            to_addrs=[to['addr'] for to in header_to],
            msg=message.as_string(),
        )
        smtp.close()
