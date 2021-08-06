#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from ._BaseModel import BaseModel


class Correction(BaseModel):
    def __init__(self, row: dict):
        self.id = row['id']
        self.day = row['day']
        self.JXLMC = row['JXLMC']
        self.jsmph = row['jsmph']
        self.JASDM = row['JASDM']
        self.SKZWS = row['SKZWS']
        self.zylxdm = row['zylxdm']
        self.jc_ks = row['jc_ks']
        self.jc_js = row['jc_js']
        self.jyytms = row['jyytms']
        self.kcm = row['kcm']
        self.SFYXZX = bool(row['SFYXZX'] == b'\x01')
