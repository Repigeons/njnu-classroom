#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from orm.BaseModel import BaseModel


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

    @property
    def json(self) -> dict:
        return dict(
            id=self.id,
            day=self.day,
            JXLMC=self.JXLMC,
            jsmph=self.jsmph,
            JASDM=self.JASDM,
            SKZWS=self.SKZWS,
            zylxdm=self.zylxdm,
            jc_ks=self.jc_ks,
            jc_js=self.jc_js,
            jyytms=self.jyytms,
            kcm=self.kcm,
            SFYXZX=self.SFYXZX,
        )
