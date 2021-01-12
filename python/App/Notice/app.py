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
            history_dir = os.path.join(os.path.dirname(Context.file), 'notice-history')
            None if os.path.exists(history_dir) else os.mkdir(history_dir)
            with open(Context.file, 'r', encoding='utf8') as f:
                data = json.load(f)
                f.close()
            history_file = os.path.join(
                history_dir,
                datetime.datetime.fromtimestamp(data['timestamp']).strftime("%Y-%m-%d %X")
            )
            shutil.copyfile(Context.file, history_file)

        # Save to notice.json
        text: str = request_args['text']
        for ch in [('\\n', '\n')]:
            text = text.replace(*ch)
        now = datetime.datetime.now()
        data = {
            'timestamp': int(now.timestamp()),
            'date': now.strftime("%Y-%m-%d"),
            'text': text,
        }
        with open(Context.file, 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False)
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
