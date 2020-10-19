#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import json
import logging
from wsgiref.simple_server import make_server
from flask import Flask, jsonify, request

import config
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
        print(type(e), e)
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


@app.route('/index.json', methods=['GET'])
def index():
    try:
        request_args = request.args.to_dict()
        response_body = request_handler.index_handler(request_args)
        return jsonify(response_body), 200
    except KeyError as e:
        return jsonify(None), 400
    except Exception as e:
        print(type(e), e)
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
        print(type(e), e)
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
        print(type(e), e)
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
        print(type(e), e)
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        request_args = request.form.to_dict()
        request_args['resultList'] = json.loads(request_args['resultList'])
        send_email(
            subject='南师教室：用户反馈',
            message=json.dumps(request_args, ensure_ascii=False, indent=2)
        )
        return jsonify(None), 202
    except Exception as e:
        print(type(e), e)
        send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}")
        return jsonify(None), 500


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-host', default='localhost', type=str, help='host to listen on')
    parser.add_argument('-port', default=8000, type=int, help='port to listen on')
    parser.add_argument('-logger', default=None, type=str, help='outputting log file')
    args = parser.parse_args()

    if config.env == 'dev':
        app.run(host=args.host, port=args.port, debug=True)
    else:
        if args.logger is not None:
            app.logger.addHandler(logging.FileHandler(args.logger))

        make_server(host=args.host, port=args.port, app=app).serve_forever()
        app.run()
