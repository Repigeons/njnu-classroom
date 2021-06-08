#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/6/8
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  EmailFile.py
""""""
from email.mime.application import MIMEApplication

from ztxlib.rpspring import Autowired
from ztxlib.rpspring import Value
from ztxlib.smtp import SMTP


class __Application:
    @Value("mail.receivers")
    def receivers(self) -> list: pass

    @Autowired
    def smtp(self) -> SMTP: pass


def email_file(
        content: bytes,
        subject: str,
):
    receivers: list = __Application.receivers
    smtp: SMTP = __Application.smtp

    mime = MIMEApplication(content)
    mime.add_header('Content-Disposition', 'attachment', filename=subject)

    smtp.send(
        subject=subject,
        header_from="Repigeons",
        header_to="南师教室运维人员",
        receivers=[receiver['addr'] for receiver in receivers],
        mime_parts=[mime]
    )
