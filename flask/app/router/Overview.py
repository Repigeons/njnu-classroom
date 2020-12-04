#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/19 0019
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Overview.py
""""""
from flask import current_app as app, request, jsonify

import utils


@app.route('/overview.json', methods=['GET'])
def overview():
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
        utils.send_email(subject='南师教室：错误报告', message=f"{type(e)}\n{e}in app.router.Overview: line 25")
        return jsonify({
            'status': -1,
            'message': f"{type(e), e}",
            'data': None
        }), 500


day_mapper = {
    0: 'sunday', 1: 'monday', 2: 'tuesday', 3: 'wednesday', 4: 'thursday', 5: 'friday', 6: 'saturday',
    'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6,
}
classrooms = {}


def reset():
    classrooms.clear()
    for jasdm in utils.database.fetchall("SELECT DISTINCT `JASDM` FROM `JAS`"):
        classrooms[jasdm[0]] = [
            {
                'jasdm': item['JASDM'],
                'JASDM': item['JASDM'],

                'jxl': item['JXLMC'],
                'JXLMC': item['JXLMC'],

                'classroom': item['jsmph'],
                'jsmph': item['jsmph'],

                'capacity': item['SKZWS'],
                'SKZWS': item['SKZWS'],

                'day': day_mapper[item['day']],
                'jc_ks': item['jc_ks'],
                'jc_js': item['jc_js'],

                'zylxdm': item['zylxdm'],
                'jyytms': item['jyytms'],
                'kcm': item['kcm'],
            } for item in
            utils.database.fetchall("SELECT * FROM `pro` WHERE `JASDM`=%(jasdm)s", {'jasdm': jasdm[0]})
        ]


def handler(args: dict) -> dict:
    if app.config['service'] == 'off':
        return {
            'status': 1,
            'message': "service off",
            'service': "off",
            'data': []
        }

    if 'jasdm' not in args.keys() or args['jasdm'] not in classrooms.keys():
        raise KeyError('jasdm')

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': classrooms[args['jasdm']]
    }


reset()
