#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/10/18 0018
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Classroom.py
""""""


class Classroom:
    def __init__(self):
        self.day = None
        self.jasdm = None
        self.jxl = None
        self.jsmph = None
        self.capacity = None
        self.zylxdm = None
        self.jc_ks = None
        self.jc_js = None
        self.jyytms = None
        self.kcm = None

    @property
    def dict(self):
        obj = self.__dict__
        obj['classroom'] = obj['jsmph']
        return obj

    @classmethod
    def load(cls, item):
        classroom = cls()
        if type(item) == dict:
            classroom.jsmph = item['jsmph']
            classroom.jxl = item['jxl']
            classroom.jasdm = item['jasdm']
            classroom.capacity = item['capacity']
            classroom.zylxdm = item['zylxdm']
            classroom.jc_ks = item['jc_ks']
            classroom.jc_js = item['jc_js']
            classroom.jyytms = item['jyytms']
            classroom.kcm = item['kcm']
        else:
            raise ValueError
        return classroom

    def __lt__(self, other):
        assert type(self) == type(other)
        if self.zylxdm != other.zylxdm:
            return self.zylxdm < other.zylxdm
        elif self.jc_js != other.jc_js:
            return self.jc_js > other.jc_js
        return self.jsmph < other.jsmph

    def __iter__(self):
        for key in self.__dict__.keys():
            yield key

    def __getitem__(self, item):
        return self.__dict__[item]
