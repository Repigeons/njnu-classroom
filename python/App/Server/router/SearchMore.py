#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  SearchMore.py
""""""
from flask import current_app as app, request, jsonify

from App.public import day_mapper, database, send_email


@app.route('/searchmore.json', methods=['GET'])
def search_more():
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
            subject="南师教室：错误报告 in app.router.SearchMore",
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

    if 'day' not in args.keys() or args['day'] != "#" and not args['day'].isdigit():
        raise KeyError('day')
    elif 'jc_ks' not in args.keys() or not args['jc_ks'].isdigit():
        raise KeyError('jc_ks')
    elif 'jc_js' not in args.keys() or not args['jc_js'].isdigit():
        raise KeyError('jc_js')
    elif 'jxl' not in args.keys():
        raise KeyError('jxl')
    elif 'zylxdm' not in args.keys():
        raise KeyError('zylxdm')
    elif 'kcm' not in args.keys():
        raise KeyError('kcm')

    jc = "`jc_ks`>=%(jc_ks)s AND `jc_js`<=%(jc_js)s"
    day = True if args['day'] == "#" else f"`day`='{day_mapper[int(args['day'])]}'"
    jxl = True if args['jxl'] == "#" else "`JXLMC`=%(jxl)s"
    zylxdm = True if args['zylxdm'] == "#" else "`zylxdm`=%(zylxdm)s"
    keyword = "`jyytms` LIKE %(keyword)s OR `kcm` LIKE %(keyword)s"
    args['keyword'] = f"%{args['kcm']}%"

    result = [
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
        database.fetchall(
            sql=f"SELECT * FROM `pro` WHERE ({day}) AND ({jc}) AND ({jxl}) AND ({zylxdm}) AND ({keyword})",
            args=args
        )
    ]

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': result
    }
