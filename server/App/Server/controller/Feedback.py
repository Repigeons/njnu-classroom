#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Feedback.py
""""""
import json
from multiprocessing import Process

from flask import current_app as app
from flask import jsonify
from flask import request
from ztxlib.rpspring import Value

from App.Server.service.Feedback import process


class __Application:
    @Value("application.server.service")
    def serve(self) -> bool: pass


@app.route('/feedback', methods=['POST'])
def route_feedback():
    if not __Application.serve:
        return None, 400
    form_data = request.form.to_dict()
    Process(
        target=process,
        kwargs={
            'jc': form_data['jc'],
            'results': json.loads(form_data['results']),
            'index': int(form_data['index']),
            'request_args': form_data,
            'jxlmc': form_data['jxl'],
            'day': int(form_data['day'])
        }
    ).start()
    return jsonify({
        'status': 0,
        'message': "ok",
        'data': "feedback"
    }), 202
