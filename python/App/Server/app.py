#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/4 0004
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  app.py
""""""
import logging
import time

from flask import Flask

start_time = time.time() * 1000
logging.info("Initializing FlaskApplication...")
app = Flask(__name__)
complete_time = time.time() * 1000
logging.info("FlaskApplication: initialization completed in %d ms", complete_time - start_time)

with app.app_context():
    from App.Server import router

    _ = router

start_time = time.time() * 1000
logging.info("Initializing Cache...")
router.reset()
complete_time = time.time() * 1000
logging.info("Cache: initialization completed in %d ms", complete_time - start_time)
