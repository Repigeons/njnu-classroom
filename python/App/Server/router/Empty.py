#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Empty.py
""""""
import json

from flask import current_app as app, request, jsonify

from App.public import day_mapper, database, get_redis, send_email


@app.route('/empty.json', methods=['GET'])
def empty():
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
            subject="南师教室：错误报告 in app.router.Empty",
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


def reset():
    redis = get_redis()
    for jxl in database.fetchall("SELECT DISTINCT `JXLDM_DISPLAY` FROM `JAS` WHERE `_SFYXZX`"):
        jxlmc = jxl[0]
        for day in range(7):
            redis.hset(
                name="Empty",
                key=f"{jxlmc}_{day}",
                value=json.dumps([
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
                    } for item in database.fetchall(
                        sql=f"SELECT * FROM `pro` "
                            f"WHERE `JXLMC`=%(JXLMC)s AND `day`=%(day)s AND `zylxdm` in ('00', '10') AND `_SFYXZX`"
                            f"ORDER BY `zylxdm`, `jc_js` DESC, `jsmph`",
                        args={'JXLMC': jxlmc, 'day': day_mapper[day]}
                    )
                ])
            )
