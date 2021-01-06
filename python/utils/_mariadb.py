#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2020/12/24 0024
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _mariadb.py
""""""
from typing import Any, List, Tuple

import mariadb


class MariaDB(mariadb.ConnectionPool):
    def __init__(
            self,
            name: str = 'pool',
            size: int = 1,
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            database: str = '',
            autocommit: bool = True,
            pool_reset_connection: bool = False,
    ):
        super().__init__(
            pool_name=name,
            pool_size=size,
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            autocommit=autocommit,
            pool_reset_connection=pool_reset_connection,
        )

    class Connection:
        class Cursor:
            def execute(self, statement: str, data: Any) -> None:
                pass

            def executemany(self, statement: str, data: List[Any]) -> None:
                pass

            def fetchone(self) -> Any:
                pass

            def fetchall(self) -> List[Any]:
                pass

        def cursor(self, *args, **kwargs) -> Cursor:
            pass

    def get_connection(self, *args, **kwargs) -> Connection:
        return super().get_connection(*args, **kwargs)

    def cursor(self) -> Tuple[Connection, Connection.Cursor]:
        connection = self.get_connection()
        return connection, connection.cursor(named_tuple=True)
