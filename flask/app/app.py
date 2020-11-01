#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import json

from flask import Flask, jsonify, request

import handler as request_handler
from utils import send_email

app = Flask(__name__)


@app.route('/reset', methods=['POST'])
def reset():
    try:
        request_handler.reset_index()
        request_handler.reset_overview()
        return jsonify(None), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


@app.route('/empty.json', methods=['GET'])
def empty():
    try:
        request_args = request.args.to_dict()
        response_body = request_handler.index_handler(request_args)
        return jsonify(response_body), 200
    except KeyError as e:
        return jsonify(None), 400
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


@app.route('/searchmore.json', methods=['GET'])
def search_more():
    try:
        request_args = request.args.to_dict()
        response_body = request_handler.searchmore_handler(request_args)
        return jsonify(response_body), 200
    except KeyError as e:
        return jsonify(None), 400
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


@app.route('/overview.json', methods=['GET'])
def overview():
    try:
        request_args = request.args.to_dict()
        response_body = request_handler.overview_handler(request_args)
        return jsonify(response_body), 200
    except KeyError as e:
        return jsonify(None), 400
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        request_args = request.form.to_dict()
        request_args['resultList'] = json.loads(request_args['resultList'])
        request_args['index'] = int(request_args['index'])
        request_args['id'] = request_args['index'] + 1
        request_args['item'] = request_args['resultList'][request_args['index']]
        send_email(
            subject='南师教室：用户反馈',
            message=json.dumps(request_args, ensure_ascii=False, indent=2)
        )
        return jsonify(None), 202
    except Exception as e:
        app.logger.warning(f"{type(e), e}")
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500
