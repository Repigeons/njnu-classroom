#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  ExceptionHandler.py
""""""
import logging

from flask import current_app as app
from flask import request
from flask import jsonify
from werkzeug.exceptions import HTTPException, InternalServerError
from ztxlib.rpspring import Autowired


class __Application:
    @Autowired
    def send_email(self) -> None: pass


@app.errorhandler(Exception)
def handle_exception(e: Exception):
    if isinstance(e, HTTPException) and not isinstance(e, InternalServerError):
        raise e
    logging.warning(f"{type(e), e}")
    __Application.send_email(
        subject="南师教室：错误报告",
        message=f"{type(e), e}\n"
                f"{request.url}\n"
                f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
    )
    return jsonify({
        'status': -1,
        'message': f"{type(e), e}",
        'data': None
    }), 500
