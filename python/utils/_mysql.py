#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2019/9/19
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _mysql
""""""
from pymysql import connect, DatabaseError


class MySQL:
    def __init__(self,
                 host='localhost',  # 要连接的主机地址
                 port=3306,  # 端口
                 user=None,  # 用于登录的数据库用户
                 password=None,  # 密码
                 database=None,  # 要连接的数据库
                 passwd=None,  # 同 password，为了兼容 MySQLdb
                 db=None,  # 同 database，为了兼容 MySQLdb
                 charset='utf8mb4',  # 字符编码
                 connect_timeout=5  # 连接超时时间，(1-31536000)
                 ):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = port
        self.__charset = charset
        self.__connect_timeout = connect_timeout
        self.__db = db
        self.__passwd = passwd

    def __connect(self) -> connect:
        """
        Private, connect to the mysql database server
        """
        return connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database,
            port=self.__port,
            charset=self.__charset,
            connect_timeout=self.__connect_timeout,
            db=self.__db,
            passwd=self.__passwd
        )

    def fetchone(self, sql: str, args=None) -> tuple or None:
        """
        Fetch the first record matches the sql sentence
        :param sql:a querying sql sentence
        :param args:a object, a tuple or a dict with the committing arguments or None
        :return:a tuple of a record
        """
        db = self.__connect()
        cursor = db.cursor()
        try:
            cursor.execute(sql, args)
            return cursor.fetchone()
        except DatabaseError:
            db.rollback()
            return None
        finally:
            db.close()

    def fetchall(self, sql: str, args=None) -> tuple or None:
        """
        Fetch all the records match the sql sentence
        :param sql:a querying sql sentence
        :param args:a object, a tuple or a dict with the committing arguments or None
        :return:a list of all the records
        """
        db = self.__connect()
        cursor = db.cursor()
        try:
            cursor.execute(sql, args)
            return cursor.fetchall()
        except DatabaseError:
            db.rollback()
            return None
        finally:
            db.close()

    def update(self, sql: str, args=None) -> int:
        """
        commit a sql sentence to modify the database
        :param sql:an updating sql sentence
        :param args:a object, a tuple or a dict with the committing arguments or None
        :return:the count of changed records
        """
        return self.update_batch((sql, args))

    def update_batch(self, *args: [tuple]) -> int:
        """
        commit some sql sentences to modify the database
        :param args: a list contains several tuple of sql and args,
            such as [(sql1,args1),(sql2,args2),...] where args may be a object, a tuple, a dict or None
        :return:
        """
        db = self.__connect()
        cursor = db.cursor()
        try:
            cnt = 0
            for sql in args:
                cnt += cursor.execute(*sql)
            db.commit()
            return cnt
        except DatabaseError:
            db.rollback()
            return 0
        finally:
            db.close()
