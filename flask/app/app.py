#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import json

from flask import Flask, jsonify, request

import utils

app = Flask(__name__)
app.config.update(
    env='pro' if app.config['ENV'] == 'production' else 'dev',
    **json.load(open('conf/config.json'))
)
with app.app_context():
    from . import router


@app.route('/reset', methods=['POST'])
def reset():
    try:
        app.logger.info("request to reset'")
        router.reset_empty()
        router.reset_overview()
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': "reset"
        }), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        utils.send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}when handle request /reset")
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        request_args = request.form.to_dict()
        request_args['resultList'] = json.loads(request_args['resultList'])
        request_args['index'] = int(request_args['index'])
        request_args['id'] = request_args['index'] + 1
        request_args['item'] = request_args['resultList'][request_args['index']]
        utils.send_email(
            subject='南师教室：用户反馈',
            message=json.dumps(request_args, ensure_ascii=False, indent=2)
        )
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': "feedback"
        }), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        utils.send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500
