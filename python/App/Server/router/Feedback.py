#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
import json

from flask import current_app as app, request, jsonify

from App.public import send_email


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        request_args = request.form.to_dict()
        request_args['resultList'] = json.loads(request_args['resultList'])
        request_args['index'] = int(request_args['index'])
        request_args['id'] = request_args['index'] + 1
        request_args['item'] = request_args['resultList'][request_args['index']]

        message = f""
        send_email(
            subject='南师教室：用户反馈',
            message=message + json.dumps(request_args, ensure_ascii=False, indent=2)
        )
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': "feedback"
        }), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}in app.app: line 63")
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


def backend():
    pass


def check_with_ehall():
    pass
