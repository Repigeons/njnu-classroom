#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import datetime
import json
import logging
import os
import shutil
import time

from flask import Flask, request, jsonify

import App.Notice._ApplicationContext as Context

start_time = time.time() * 1000
logging.info("Initializing FlaskApplication...")
app = Flask(__name__)
complete_time = time.time() * 1000
logging.info("FlaskApplication: initialization completed in %d ms", complete_time - start_time)


@app.route('/', methods=['PUT'])
def index():
    try:
        request_args: dict = request.form.to_dict()
        request_headers: dict = request.headers.environ
        if 'text' not in request_args.keys():
            raise KeyError("Expected field `text`")
        if 'HTTP_TOKEN' not in request_headers.keys():
            raise KeyError("Expected field `token`")
        if Context.token != request_headers['HTTP_TOKEN']:
            raise ValueError("Invalid token")

        # Save to notice history
        if os.path.exists(Context.file):
            file = os.path.abspath(Context.file)
            history = os.path.join(os.path.dirname(file), f"_{os.path.basename(file)}")
            history_list = json.load(open(history, encoding='utf8')) if os.path.exists(history) else []
            history_list.append(json.load(open(Context.file, encoding='utf8')))
            json.dump(history_list, open(history, 'w', encoding='utf8'))

        # Save to [notice.json]
        text: str = request_args['text']
        for ch in [('\\n', '\n')]:
            text = text.replace(*ch)
        now = datetime.datetime.now()
        data = {
            'timestamp': int(now.timestamp()),
            'date': now.strftime("%Y-%m-%d"),
            'text': text,
        }
        json.dump(
            obj=data,
            fp=open(Context.file, 'w', encoding='utf8'),
            ensure_ascii=False,
            indent=2
        )
        return jsonify({
            'status': 0,
            'message': "ok",
            'data': data
        }), 202
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
