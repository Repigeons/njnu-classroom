#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import datetime
import json
import os
import shutil

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.update(
    env=os.getenv("env"),
    **json.load(open(f"{os.getenv('conf', 'conf')}/notice.json"))
)


@app.route('/', methods=['PUT'])
def index():
    token = app.config['token']
    file = app.config['file']

    try:
        request_args: dict = request.form.to_dict()
        request_headers: dict = request.headers.environ
        if 'text' not in request_args.keys():
            raise KeyError("Expected field `text`")
        if 'HTTP_TOKEN' not in request_headers.keys():
            raise KeyError("Expected field `token`")
        if token != request_headers['HTTP_TOKEN']:
            raise ValueError("Invalid token")

        # Save to notice history
        if os.path.exists(file):
            history_dir = os.path.join(os.path.dirname(file), 'notice-history')
            None if os.path.exists(history_dir) else os.mkdir(history_dir)
            with open(file, 'r', encoding='utf8') as f:
                data = json.load(f)
                f.close()
            history_file = os.path.join(
                history_dir,
                datetime.datetime.fromtimestamp(data['timestamp']).strftime("%Y-%m-%d %X")
            )
            shutil.copyfile(file, history_file)

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
        with open(file, 'w', encoding='utf8') as f:
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
        app.logger.warning(f"{type(e), e}")
        return jsonify({
            'status': 1,
            'message': type(e),
            'detail': e.args[0]
        }), 500
