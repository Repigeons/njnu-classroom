#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import re

from .BaseModel import BaseModel


class JAS(BaseModel):
    def __init__(self, row: dict):
        self.JASDM = row['JASDM']
        self.JASMC = row['JASMC']
        self.JXLDM = row['JXLDM']
        self.JXLMC = row['JXLDM_DISPLAY']
        self.XXXQDM = row['XXXQDM']
        self.XXXQDM_DISPLAY = row['XXXQDM_DISPLAY']
        self.JASLXDM = row['JASLXDM']
        self.JASLXDM_DISPLAY = row['JASLXDM_DISPLAY']
        self.ZT = row['ZT']
        self.LC = row['LC']
        self.JSYT = row['JSYT']
        self.SKZWS = row['SKZWS']
        self.KSZWS = row['KSZWS']
        self.XNXQDM = row['XNXQDM']
        self.XNXQDM2 = row['XNXQDM2']
        self.DWDM = row['DWDM']
        self.DWDM_DISPLAY = row['DWDM_DISPLAY']
        self.ZWSXDM = row['ZWSXDM']
        self.XGDD = row['XGDD']
        self.SYRQ = row['SYRQ']
        self.SYSJ = row['SYSJ']
        self.SXLB = row['SXLB']
        self.BZ = row['BZ']
        self.SFYPK = bool(row['SFYPK'] == b'\x01')
        self.SFYXPK = bool(row['SFYXPK'] == b'\x01')
        self.PKYXJ = row['PKYXJ']
        self.SFKSWH = bool(row['SFKSWH'] == b'\x01')
        self.SFYXKS = bool(row['SFYXKS'] == b'\x01')
        self.KSYXJ = row['KSYXJ']
        self.SFYXCX = bool(row['SFYXCX'] == b'\x01')
        self.SFYXJY = bool(row['SFYXJY'] == b'\x01')
        self.SFYXZX = bool(row['SFYXZX'] == b'\x01')
        self.jsmph = re.sub(pattern='^' + self.JXLMC, repl='', string=self.JASMC)
