#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Overview.py
""""""
import json

from flask import current_app as app, request, jsonify

from App.public import get_redis, send_email


@app.route('/overview.json', methods=['GET'])
def route():
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
        app.logger.warning(f"{type(e), e}")
        send_email(
            subject="南师教室：错误报告 in app.router.Overview",
            message=f"{type(e), e}\n"
                    f"{request.url}\n"
        )
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


def handler(args: dict) -> dict:
    if app.config['service'] == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    redis = get_redis()

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
