#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/20 0020
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Notice.py
""""""
import json
import os
from datetime import datetime
from wsgiref.simple_server import make_server

from flask import Flask, jsonify, request

app = Flask(__name__)

token = os.getenv('NOTICE_TOKEN')
file = os.getenv('NOTICE_FILE')


@app.route('/', methods=['PUT'])
def main():
    try:
        request_args: dict = request.form.to_dict()
        if 'token' not in request_args.keys():
            raise KeyError("Expected field `token`")
        if 'text' not in request_args.keys():
            raise KeyError("Expected field `text`")
        if token != request_args['token']:
            raise ValueError("incorrect token")

        text: str = request_args['text']
        text = text.replace('\\n', '\n')

        now = datetime.now()
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


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-host', default='localhost', type=str, help='host to listen on')
    parser.add_argument('-port', default=8008, type=int, help='port to listen on')
    args = parser.parse_args()

    make_server(host=args.host, port=args.port, app=app).serve_forever()
    app.run()
