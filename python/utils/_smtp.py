#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/7/17 0017
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _smtp.py
""""""
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL, SMTPRecipientsRefused
from typing import List


class SMTP:
    class NonReceiversError(TypeError or SMTPRecipientsRefused):
        pass

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
            header_from: str = '',
            header_to: str = '',
            receivers: List[str] = None,
            mime_parts: List[MIMEBase] = None
    ):
        if receivers is None:
            raise SMTP.NonReceiversError("unresolved receivers: [%s]" % receivers)
        if len(receivers) == 0:
            raise SMTP.NonReceiversError("empty receivers: %s" % receivers)

        message = MIMEMultipart()
        message['Subject'] = Header(subject)
        message['From'] = Header(f"{header_from}<{self.__user}>")
        message['To'] = Header(header_to)
        if mime_parts is not None:
            for mime_part in mime_parts:
                message.attach(mime_part)

        server = SMTP_SSL(host=self.__host, port=self.__port)
        server.login(user=self.__user, password=self.__password)
        server.sendmail(from_addr=self.__user, to_addrs=receivers, msg=message.as_string())
        server.quit()
