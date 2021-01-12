#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Empty.py
""""""
import json
import logging

from flask import current_app as app, request, jsonify
from redis import StrictRedis

import App.Server._ApplicationContext as Context

from App.Server._ApplicationContext import send_email


@app.route('/empty.json', methods=['GET'])
def route_empty():
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
    if Context.service == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    redis = StrictRedis(connection_pool=Context.redis_pool)

    if 'day' not in args.keys() or not args['day'].isdigit() or not (0 <= int(args['day']) <= 6):
        raise KeyError('day')
    elif 'dqjc' not in args.keys() or not args['dqjc'].isdigit():
        raise KeyError('dqjc')
    elif 'jxl' not in args.keys() or not redis.hexists("Empty", f"{args['jxl']}_{args['day']}"):
        raise KeyError('jxl')

    jxl, day, dqjc = args['jxl'], int(args['day']), int(args['dqjc'])

    value = json.loads(redis.hget(
        name="Empty",
        key=f"{args['jxl']}_{args['day']}"
    ))

    classrooms = []
    for classroom in value:
        if classroom['jc_ks'] <= dqjc <= classroom['jc_js']:
            classrooms.append(classroom)
    for i in range(len(classrooms)):
        classrooms[i]['id'] = classrooms[i]['rank'] = i + 1

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': classrooms
    }
