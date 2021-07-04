#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/24 0024
# @Author   :  ZhouTianxing
# @Software :  PyCharm Professional x64
# @FileName :  _mariadb
""""""
from typing import Any
from typing import List
from typing import NamedTuple
from typing import Tuple

import mariadb


class MariaDB(mariadb.ConnectionPool):
    def __init__(
            self,
            name: str = 'pool',  # 连接池名称
            host: str = 'localhost',  # 数据库地址
            port: int = 3306,  # 数据库端口
            user: str = 'root',  # 用户名
            password: str = '',  # 密码
            database: str = '',  # 数据库名称
            autocommit: bool = True,
    ):
        super().__init__(
            pool_name=name,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=autocommit,
        )
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.autocommit = autocommit

    def __str__(self):
        return f"MariadbConnectionPool<host={self.host},port={self.port},database={self.database}>"

    class Connection:
        class Cursor:
            def execute(self, statement: str, data: Any) -> None:
                pass

            def executemany(self, statement: str, data: List[Any]) -> None:
                pass

            def fetchone(self) -> NamedTuple:
                pass

            def fetchall(self) -> List[NamedTuple]:
                pass

            def close(self) -> None:
                pass

        def cursor(self, *args, **kwargs) -> Cursor:
            pass

        def close(self) -> None:
            pass

    def get_connection(self, *args, **kwargs) -> Connection:
        try:
            connection = super().get_connection(*args, **kwargs)
            return connection
        except mariadb.PoolError:
            connection = mariadb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                autocommit=self.autocommit,
            )
            try:
                self.add_connection(connection)
            except mariadb.PoolError:
                pass
            return connection

    def get_connection_cursor(self) -> Tuple[Connection, Connection.Cursor]:
        connection = self.get_connection()
        cursor = connection.cursor(named_tuple=True)
        return connection, cursor
