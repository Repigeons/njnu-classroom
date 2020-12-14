#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import json
import os

from flask import Flask, jsonify

from App.public import send_email

app = Flask(__name__)
app.config.update(
    env=os.getenv("env"),
    **json.load(open('conf/server.json'))
)
with app.app_context():
    from App.Server import router


@app.route('/reset', methods=['POST'])
def reset():
    try:
        app.logger.info("request to reset'")
        router.reset()
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': "reset"
        }), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}in app.app: line 35")
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


router.reset()
