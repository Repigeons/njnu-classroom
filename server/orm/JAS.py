#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import re

from orm.BaseModel import BaseModel


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

    @property
    def json(self) -> dict:
        return dict(
            JASDM=self.JASDM,
            JASMC=self.JASMC,
            JXLDM=self.JXLDM,
            JXLMC=self.JXLMC,
            XXXQDM=self.XXXQDM,
            XXXQDM_DISPLAY=self.XXXQDM_DISPLAY,
            JASLXDM=self.JASLXDM,
            JASLXDM_DISPLAY=self.JASLXDM_DISPLAY,
            ZT=self.ZT,
            LC=self.LC,
            JSYT=self.JSYT,
            SKZWS=self.SKZWS,
            KSZWS=self.KSZWS,
            XNXQDM=self.XNXQDM,
            XNXQDM2=self.XNXQDM2,
            DWDM=self.DWDM,
            DWDM_DISPLAY=self.DWDM_DISPLAY,
            ZWSXDM=self.ZWSXDM,
            XGDD=self.XGDD,
            SYRQ=self.SYRQ,
            SYSJ=self.SYSJ,
            SXLB=self.SXLB,
            BZ=self.BZ,
            SFYPK=self.SFYPK,
            SFYXPK=self.SFYXPK,
            PKYXJ=self.PKYXJ,
            SFKSWH=self.SFKSWH,
            SFYXKS=self.SFYXKS,
            KSYXJ=self.KSYXJ,
            SFYXCX=self.SFYXCX,
            SFYXJY=self.SFYXJY,
            SFYXZX=self.SFYXZX,
            jsmph=self.jsmph,
        )
