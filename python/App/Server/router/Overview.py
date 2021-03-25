#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Overview.py
""""""
import json
import logging

from flask import current_app as app, request, jsonify
from redis import StrictRedis
from redis_lock import Lock

from utils.aop import autowired, configuration


@autowired()
def send_email(subject: str, message: str): _ = subject, message


@autowired()
def redis_pool(): pass


@configuration("application.server.service")
def serve(): pass


@app.route('/overview.json', methods=['GET'])
def route_overview():
    try:
        request_args = request.args.to_dict()
        response_body = handler(request_args)
        return jsonify(response_body), 200
    except KeyError as e:
        return jsonify({
            'status': 2,
            'message': f"Expected or unresolved key `{e}`",
            'data': []
        }), 400
    except Exception as e:
        logging.warning(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告",
            message=f"{type(e), e}\n"
                    f"{request.url}\n"
                    f"{e.__traceback__.tb_frame.f_globals['__file__']}:{e.__traceback__.tb_lineno}\n"
        )
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


def handler(args: dict) -> dict:
    if not serve:
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    redis = StrictRedis(connection_pool=redis_pool)
    lock = Lock(redis, "Server-Overview")
    if lock.acquire():
        try:
            if 'jasdm' not in args.keys() or not redis.hexists("Overview", args['jasdm']):
                raise KeyError('jasdm')

            value = json.loads(redis.hget(
                name="Overview",
                key=args['jasdm']
            ))

            return {
                'status': 0,
                'message': "ok",
                'service': "on",
                'data': value
            }
        finally:
            lock.release()
