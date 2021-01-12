#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  SearchMore.py
""""""
import logging

from flask import current_app as app, request, jsonify

import App.Server._ApplicationContext as Context

from App.Server._ApplicationContext import send_email


@app.route('/searchmore.json', methods=['GET'])
def route_search_more():
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
    day = True if args['day'] == "#" else f"`day`='{Context.day_mapper[int(args['day'])]}'"
    jxl = True if args['jxl'] == "#" else "`JXLMC`=%(jxl)s"
    zylxdm = True if args['zylxdm'] == "#" else "`zylxdm`=%(zylxdm)s"
    keyword = "`jyytms` LIKE %(keyword)s OR `kcm` LIKE %(keyword)s"
    args['keyword'] = f"%{args['kcm']}%"

    connection, cursor = Context.mysql.get_connection_cursor()
    cursor.execute(f"SELECT * FROM `pro` WHERE ({day}) AND ({jc}) AND ({jxl}) AND ({zylxdm}) AND ({keyword})", args)
    result = [
        {
            'jasdm': row.JASDM,
            'JASDM': row.JASDM,

            'jxl': row.JXLMC,
            'JXLMC': row.JXLMC,

            'classroom': row.jsmph,
            'jsmph': row.jsmph,

            'capacity': row.SKZWS,
            'SKZWS': row.SKZWS,

            'day': Context.day_mapper[row.day],
            'jc_ks': row.jc_ks,
            'jc_js': row.jc_js,

            'zylxdm': row.zylxdm,
            'jyytms': row.jyytms,
            'kcm': row.kcm,
        } for row in cursor.fetchall()
    ]
    cursor.close(), connection.close()

    return {
        'status': 0,
        'message': "ok",
        'service': "on",
        'data': result
    }
