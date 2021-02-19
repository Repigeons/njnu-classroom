#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/13 0013
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Shuttle.py
""""""
from flask import current_app as app, request, jsonify

import App.Explore._ApplicationContext as Context


@app.route('/shuttle.json', methods=['GET'])
def shuttle():
    return jsonify(Context.shuttle)
