#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/11 0011
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.update(
    env=os.getenv("env"),
    **json.load(open('conf/explore.json'))
)
with app.app_context():
    from .router import Shuttle
