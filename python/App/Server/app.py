#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import json
import os

from flask import Flask

app = Flask(__name__)
app.config.update(
    env=os.getenv("env"),
    **json.load(open(f"{os.getenv('conf', 'conf')}/server.json"))
)
with app.app_context():
    from App.Server import router

router.reset()
