#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

import aiosmtplib


class NonReceiversError(TypeError):
    pass


class SMTP:
    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
    ):
        """

        :param host: 发件服务器地址
        :param port: 发件服务器端口号
        :param user: 用户名（发件人地址）
        :param password: 密码
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    async def __aenter__(self) -> 'SMTP':
        self.smtp = aiosmtplib.SMTP()
        await self.smtp.connect(
            hostname=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            use_tls=True
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.smtp.quit()

    async def send(
            self,
            subject: str,
            header_from: str = '',
            header_to: str = '',
            receivers: list[str] = None,
            mime_parts: list[MIMEBase] = None
    ) -> None:
        """
        发送邮件

        :param subject: 邮件主题
        :param header_from: 发件人名称
        :param header_to: 收件人名称
        :param receivers: 收件人地址
        :param mime_parts: 邮件内容
        :return:
        """
        if not isinstance(receivers, list):
            raise NonReceiversError("unresolved receivers: [%s]" % receivers)
        if len(receivers) == 0:
            raise NonReceiversError("empty receivers: %s" % receivers)

        message = MIMEMultipart()
        message['Subject'] = Header(subject)
        message['From'] = Header("%s<%s>" % (header_from, self.user))
        message['To'] = Header(header_to)
        if mime_parts is not None:
            for mime_part in mime_parts:
                message.attach(mime_part)

        await self.smtp.sendmail(
            sender=self.user,
            recipients=receivers,
            message=message.as_string()
        )
