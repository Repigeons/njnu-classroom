#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
import aiomysql


class MySQL:
    @classmethod
    async def create_pool(cls,
                          host: str = 'localhost',
                          port: int = 3306,
                          user: str = 'root',
                          password: str = '',
                          database: str = '',
                          ) -> 'MySQL':
        """
        创建 MySQL 异步连接池

        :param host: 数据库地址
        :param port: 数据库端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名称
        :return:
        """

        return cls(await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
        ))

    def __init__(self, pool: aiomysql.Pool = None):
        self.pool = pool

    async def execute(self,
                      statement: str,
                      *args: dict,
                      ) -> int:
        """
        提交一条或多条修改操作

        :param statement: SQL语句
        :param args: SQL参数
        :return: 修改记录数
        """

        if not isinstance(self.pool, aiomysql.Pool):
            raise aiomysql.Error

        conn: aiomysql.Connection
        cursor: aiomysql.Cursor
        rows = 0
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.Cursor) as cursor:
                if len(args) == 0:
                    await cursor.execute(statement)
                for data in args:
                    rows += await cursor.execute(statement, data)
                await conn.commit()
                return rows

    async def fetchone(self,
                       statement: str,
                       data: dict = None
                       ) -> dict:
        """
        查询一条结果

        :param statement: SQL语句
        :param data: SQL参数
        :return: 查询结果
        """
        if not isinstance(self.pool, aiomysql.Pool):
            raise aiomysql.Error

        conn: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(statement, data)
                return await cursor.fetchone()

    async def fetchall(self,
                       statement: str,
                       data: dict = None
                       ) -> list[dict]:
        """
        查询多条结果

        :param statement: SQL语句
        :param data: SQL参数
        :return: 查询结果
        """
        if not isinstance(self.pool, aiomysql.Pool):
            raise aiomysql.Error

        conn: aiomysql.Connection
        cursor: aiomysql.DictCursor

        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(statement, data)
                return await cursor.fetchall()
