#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Search.py
""""""
from flask import current_app as app
from flask import jsonify
from flask import request

from App.Server.service import handle_search


@app.route('/searchmore.json', methods=['GET'])
def route_search():
    try:
        return jsonify(
            handle_search(args=request.args.to_dict())
        ), 200
    except KeyError as e:
        return jsonify({
            'status': 2,
            'message': f"Expected or unresolved key `{e}`",
            'data': []
        }), 400
