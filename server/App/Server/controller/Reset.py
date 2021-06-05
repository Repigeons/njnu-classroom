#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/15 0015
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Reset.py
""""""
from threading import Thread

from flask import current_app as app
from flask import jsonify

from App.Server.service import reset


@app.route('/reset', methods=['POST'])
def route_reset():
    Thread(target=reset).start()
    return jsonify({
        'status': 0,
        'message': "ok",
        'data': "reset"
    }), 202
