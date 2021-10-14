#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from ._BaseModel import BaseModel


class KCB(BaseModel):
    def __init__(self, row: dict):
        self.id: int = row['id']
        self.day: str = row['day']
        """Enum('Sun.','Mon.','Tue.','Wed.','Thu.','Fri.','Sat.')"""
        self.JXLMC: str = row['JXLMC']
        """教学楼名称"""
        self.jsmph: str = row['jsmph']
        """教室门牌号"""
        self.JASDM: str = row['JASDM']
        """教室代码"""
        self.SKZWS: int = row['SKZWS']
        """上课座位数"""
        self.zylxdm: str = row['zylxdm']
        """资源类型代码"""
        self.jc_ks: int = row['jc_ks']
        """开始节次"""
        self.jc_js: int = row['jc_js']
        """结束节次"""
        self.jyytms: str = row['jyytms']
        """借用用途说明"""
        self.kcm: str = row['kcm']
        """课程名"""
        self.SFYXZX: bool = bool(row['SFYXZX'] == b'\x01')
        """是否允许自习"""
