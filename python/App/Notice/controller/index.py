#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/3/26
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  index.py
""""""
import logging

from flask import current_app as app
from flask import request
from flask import jsonify

from App.Notice.service import handle


@app.route('/', methods=['PUT'])
def index():
    try:
        return jsonify(handle(
            form_data=request.form.to_dict(),
            headers=request.headers.environ
        )), 200
    except KeyError as e:
        return jsonify({
            'status': 1,
            'message': "KeyError",
            'detail': e.args[0]
        }), 400
    except ValueError as e:
        return jsonify({
            'status': 1,
            'message': "TokenError",
            'detail': e.args[0]
        }), 403
    except Exception as e:
        logging.warning(
            f"{type(e), e}"
            f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        return jsonify({
            'status': 1,
            'message': type(e),
            'detail': e.args[0]
        }), 500
