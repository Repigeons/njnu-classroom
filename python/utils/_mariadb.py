#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/24 0024
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _mariadb.py
""""""
from typing import Any, List, Tuple, NamedTuple

import mariadb


class MariaDB(mariadb.ConnectionPool):
    def __init__(
            self,
            name: str = 'pool',
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            database: str = '',
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
            self.add_connection(connection)
            return connection

    def get_connection_cursor(self) -> Tuple[Connection, Connection.Cursor]:
        connection = self.get_connection()
        cursor = connection.cursor(named_tuple=True)
        return connection, cursor
