#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/8/7
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from app import app
from ztxlib import aiomysql


class PageResult:
    def __init__(self,
                 result: list,
                 count: int,
                 page_num: int,
                 page_size: int,
                 ):
        self.total = count
        self.totalPage = int((count - 1) / page_size) + 1
        self.pageNum = page_num
        self.pageSize = page_size
        self.list = result

    def map(self, orm_type) -> 'PageResult':
        self.list = [orm_type(item).dict for item in self.list]
        return self

    @classmethod
    async def rest(cls,
                   table: str,
                   where: str = None,
                   order: str = None,
                   data: dict = None,
                   *,
                   page_num: int,
                   page_size: int,
                   ) -> 'PageResult':
        where = f"WHERE {where}" if where else ""
        order = f"ORDER BY {order}" if order else ""
        clause = f"{where} {order}"
        if data is None:
            data = dict()
        data.update(
            __page_size=page_size,
            __page_offset=page_num * page_size,
        )
        result = await cls.__get_data(
            table=table,
            clause=clause,
            data=data,
        )
        count = await cls.__get_count(
            table=table,
            clause=clause,
            data=data,
        )
        return cls(
            result=result,
            count=count,
            page_num=page_num,
            page_size=page_size,
        )

    @classmethod
    async def __get_data(cls,
                         table: str,
                         clause: str,
                         data: dict):
        mysql: aiomysql.MySQL = app['mysql']
        return await mysql.fetchall(
            f"SELECT * FROM `{table}` {clause} LIMIT %(__page_size)s OFFSET %(__page_offset)s",
            data=data
        )

    @classmethod
    async def __get_count(cls,
                          table: str,
                          clause: str,
                          data: dict) -> int:
        mysql: aiomysql.MySQL = app['mysql']
        result = await mysql.fetchone(
            f"SELECT COUNT(*) AS `count` FROM `{table}` {clause}",
            data=data
        )
        return result['count']

    @property
    def dict(self) -> dict:
        return dict(
            total=self.total,
            totalPage=self.totalPage,
            pageNum=self.pageNum,
            pageSize=self.pageSize,
            list=self.list,
        )
